#!/usr/bin/env python3
import argparse, json, re, socket, ssl, sys, time
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag
from datetime import datetime, timezone

import requests, yaml
from bs4 import BeautifulSoup

UA = "WebsiteMaintenanceAudit/1.0"

def result(id_, label, status, method, summary, details=None, evidence=None):
    return {"id": id_, "label": label, "status": status, "method": method,
            "summary": summary, "details": details or [], "evidence": evidence or []}

def normalize(url):
    u,_ = urldefrag(url)
    p=urlparse(u)
    if p.scheme not in ("http","https"): return None
    return u

def fetch(session, url, timeout):
    try:
        r=session.get(url, timeout=timeout, allow_redirects=True)
        return r, None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"

def crawl(base, max_pages, timeout):
    origin=urlparse(base).netloc
    s=requests.Session(); s.headers.update({"User-Agent":UA})
    q=[base]; seen=set(); pages={}; discovered_links=[]
    while q and len(seen)<max_pages:
        url=q.pop(0)
        if url in seen: continue
        seen.add(url)
        r,err=fetch(s,url,timeout)
        pages[url]={"status": None if err else r.status_code, "error":err, "final_url":None if err else r.url}
        if err or not r or "text/html" not in r.headers.get("content-type",""): continue
        soup=BeautifulSoup(r.text,"html.parser")
        pages[url]["html"]=r.text
        for a in soup.find_all("a", href=True):
            target=normalize(urljoin(r.url,a["href"].strip()))
            if not target: continue
            discovered_links.append((url,target))
            if urlparse(target).netloc==origin and target not in seen and target not in q:
                q.append(target)
    return s,pages,discovered_links

def check_links(session, links, timeout):
    checked={}; bad=[]; restricted=[]
    for src,target in links:
        if target in checked: continue
        try:
            r=session.get(target, timeout=timeout, allow_redirects=True, stream=True)
            code=r.status_code
            checked[target]=code
            if code in (401,403): restricted.append({"source":src,"target":target,"status":code})
            elif code>=400: bad.append({"source":src,"target":target,"status":code})
        except Exception as e:
            checked[target]=str(e); bad.append({"source":src,"target":target,"error":str(e)})
    if bad:
        return result("links","Links","fail","automatic",f"{len(bad)} fehlerhafte Links gefunden.",bad)
    msg=f"{len(checked)} eindeutige HTTP(S)-Links geprüft; keine eindeutigen Dead Links gefunden."
    if restricted: msg += f" {len(restricted)} Links antworteten mit 401/403 und wurden nicht als dead gewertet."
    return result("links","Links","pass","automatic",msg,restricted)

def find_legal(pages, terms, label, id_):
    for url,data in pages.items():
        if data.get("status") and data["status"]<400:
            txt=BeautifulSoup(data.get("html",""),"html.parser").get_text(" ", strip=True).lower()
            path=urlparse(url).path.lower()
            if any(t in path or t in txt[:1000] for t in terms):
                return result(id_,label,"pass","automatic",f"Erreichbare Seite gefunden: {url}",[url])
    return result(id_,label,"fail","automatic","Keine eindeutig erreichbare passende Seite im Crawl gefunden.")

def detect_versions(pages):
    wp=[]; php=[]
    for url,data in pages.items():
        html=data.get("html","")
        for m in re.findall(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']WordPress\s+([^"\']+)', html, flags=re.I): wp.append(m.strip())
        for m in re.findall(r'[?&]ver=(\d+\.\d+(?:\.\d+)?)', html):
            if "wp-" in html.lower(): wp.append(m)
    wpv=max(wp, key=len) if wp else None
    return wpv, None

def google_fonts(pages):
    hits=[]
    for url,data in pages.items():
        html=data.get("html","").lower()
        for host in ("fonts.googleapis.com","fonts.gstatic.com"):
            if host in html: hits.append({"page":url,"host":host})
    if hits: return result("google_fonts","Google Fonts local Hosting","fail","automatic","Google-Fonts-Hosts wurden im geladenen HTML gefunden.",hits)
    return result("google_fonts","Google Fonts local Hosting","pass","automatic","Keine direkten Google-Fonts-Hosts im gecrawlten HTML gefunden. Netzwerkprüfung per Playwright folgt separat.")

def ssl_check(url, warning_days):
    host=urlparse(url).hostname; port=urlparse(url).port or 443
    try:
        ctx=ssl.create_default_context()
        with socket.create_connection((host,port),timeout=10) as sock:
            with ctx.wrap_socket(sock,server_hostname=host) as ssock:
                cert=ssock.getpeercert()
        exp=datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        days=(exp-datetime.now(timezone.utc)).days
        st="warning" if days<warning_days else "pass"
        return result("ssl","SSL-Gültigkeitsprüfung",st,"automatic",f"TLS-Zertifikat gültig bis {exp.date().isoformat()} ({days} Tage).")
    except Exception as e:
        return result("ssl","SSL-Gültigkeitsprüfung","fail","automatic",f"SSL-Prüfung fehlgeschlagen: {e}")

def visual_checks(cfg, outdir):
    if not cfg.get("visual",{}).get("enabled", True):
        return []
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return [result(k,l,"manual","automatic","Playwright ist nicht installiert.") for k,l in [
            ("desktop","Desktop"),("mobile","Mobile"),("tablet_landscape","IPad Landscape"),("tablet_portrait","IPad Portrait")]]
    base=cfg["site"]["url"]; pages=cfg["visual"].get("representative_pages",["/"])
    vps=cfg["visual"].get("viewports",{})
    labels={"desktop":"Desktop","mobile":"Mobile","tablet_landscape":"IPad Landscape","tablet_portrait":"IPad Portrait"}
    shots=Path(outdir)/"evidence"/"screenshots"; shots.mkdir(parents=True,exist_ok=True)
    outcomes=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            for key,label in labels.items():
                vp=vps.get(key)
                if not vp: outcomes.append(result(key,label,"manual","automatic","Kein Viewport konfiguriert.")); continue
                issues=[]; evidence=[]
                ctx=browser.new_context(viewport={"width":vp[0],"height":vp[1]})
                for rel in pages:
                    page=ctx.new_page(); url=urljoin(base,rel)
                    try:
                        page.goto(url, wait_until="networkidle", timeout=30000)
                        overflow=page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth + 2")
                        if overflow: issues.append(f"Horizontaler Overflow auf {url}")
                        fn=f"{key}-{re.sub(r'[^a-zA-Z0-9]+','_',rel).strip('_') or 'home'}.png"
                        path=shots/fn; page.screenshot(path=str(path), full_page=True); evidence.append(str(path))
                    except Exception as e: issues.append(f"{url}: {e}")
                    finally: page.close()
                ctx.close()
                outcomes.append(result(key,label,"warning" if issues else "pass","automatic+visual",
                    "Screenshots erstellt; " + ("Auffälligkeiten erkannt." if issues else "keinen horizontalen Overflow erkannt. Visuelle Agentenprüfung erforderlich."), issues,evidence))
            browser.close()
    except Exception as e:
        return [result(k,l,"manual","automatic",f"Playwright konnte nicht ausgeführt werden: {e}") for k,l in labels.items()]
    return outcomes

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("config"); ap.add_argument("--out",default="audit-output")
    args=ap.parse_args(); cfg=yaml.safe_load(Path(args.config).read_text())
    out=Path(args.out); (out/"evidence").mkdir(parents=True,exist_ok=True)
    base=cfg["site"]["url"]; timeout=cfg.get("crawl",{}).get("timeout_seconds",15)
    sess,pages,links=crawl(base,cfg.get("crawl",{}).get("max_pages",100),timeout)
    results=[]
    results.append(result("navigation","Buttons / Navigation","pass" if pages.get(base,{}).get("status",999)<400 else "fail","automatic","Startseite und Navigation wurden gecrawlt; interaktive Geschäftsprozesse sind hiervon nicht vollständig abgedeckt."))
    results.append(check_links(sess,links,timeout))
    results.append(find_legal(pages,["impressum","anbieterkennzeichnung"],"Impressum vorhanden","impressum"))
    results.append(find_legal(pages,["datenschutz","privacy"],"Datenschutz vorhanden","datenschutz"))
    results.append(google_fonts(pages))
    wpv,_=detect_versions(pages)
    results.append(result("wordpress","WordPress","pass" if wpv else "not_verifiable","automatic",f"Öffentlich erkannte WordPress-Version: {wpv}" if wpv else "WordPress-Version öffentlich nicht zuverlässig erkennbar."))
    results.append(result("php","PHP","not_verifiable","automatic","PHP-Version wird ohne serverseitige/authentifizierte Quelle nicht geraten. Prüfe WP Site Health, WP-CLI oder Hosting-API."))
    results.extend(visual_checks(cfg,out))
    results.append(result("dsgvo_check","Dr. DSGVO Webseiten Check","manual","manual","Externer Dienst; manuelle Ausführung oder dedizierte Integration erforderlich."))
    results.append(result("backup","Backup","not_verifiable","authenticated","Backup kann öffentlich nicht verifiziert werden. Hosting-/Plugin-/Backup-Zugriff erforderlich."))
    results.append(ssl_check(base,cfg.get("ssl",{}).get("warning_days_before_expiry",30)))
    data={"site":cfg["site"],"audit_date":datetime.now().astimezone().strftime("%d.%m.%Y"),"audit_month":datetime.now().astimezone().strftime("%B %Y"),"pages_crawled":len(pages),"results":results}
    (out/"audit-results.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    print(out/"audit-results.json")
if __name__=="__main__": main()
