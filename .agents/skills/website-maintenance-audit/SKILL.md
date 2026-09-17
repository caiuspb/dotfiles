---
name: website-maintenance-audit
description: Automatisiert wiederkehrende Website-Wartungsaudits: Links, Navigation, Impressum, Datenschutz, Google Fonts, Responsive-Darstellung, SSL, WordPress/PHP soweit verifizierbar, Backup-Status und DOCX-Bericht. Verwenden, wenn eine Kundenwebsite im Rahmen eines Wartungsvertrags geprüft und dokumentiert werden soll.
---

# Website Maintenance Audit

## Ziel

Führe einen reproduzierbaren Website-Wartungsaudit durch und erzeuge einen kundenfertigen DOCX-Bericht aus `assets/audit-template.docx`.

## Ablauf

1. Ermittle die gewünschte Kundenkonfiguration. Liegt keine `config.yaml` vor, kopiere `config.example.yaml` und passe URL/Name an.
2. Installiere Abhängigkeiten nur falls notwendig: `pip install -r requirements.txt` und für visuelle Tests `playwright install chromium`.
3. Starte `scripts/run_audit.sh <config>`.
4. Prüfe `audit-results.json` und die Screenshots unter `evidence/screenshots/`.
5. Bewerte Screenshots tatsächlich visuell. Ein vorhandener Screenshot ist noch kein Beweis für korrektes Layout.
6. Korrigiere Statuswerte bei eindeutig sichtbaren Layoutfehlern und generiere den Bericht erneut.
7. Öffne/rendere den erzeugten DOCX-Bericht und prüfe Layout, Tabellen, Logo, Statussymbole und Footer vor Auslieferung.

## Statusregeln

- `pass`: durch Belege verifiziert
- `warning`: Prüfung möglich, aber Auffälligkeit oder menschliche Sichtprüfung nötig
- `fail`: eindeutiger Fehler
- `manual`: bewusst manuell auszuführender Check
- `not_verifiable`: ohne zusätzliche Zugriffsrechte nicht seriös prüfbar

Niemals einen Punkt grün markieren, wenn keine Evidenz existiert.

## PHP

Die PHP-Version nicht raten. Öffentlich sichtbare Header sind nur ein Hinweis. Für eine zuverlässige Version bevorzugen:

- WordPress Site Health mit authentifizierter Sitzung
- `wp eval 'echo PHP_VERSION;'`
- Hosting-API/Panel

`php -v` kann von der PHP-Version des Webservers abweichen.

## WordPress

Öffentliche Fingerprints sind nur Best Effort. Für zuverlässige Daten bevorzugen:

- `wp core version`
- WordPress Site Health
- Hosting-/Management-API

Updates niemals automatisch durchführen, wenn der Auftrag nur ein Audit ist.

## Backup

Ein Backup kann nicht über die öffentliche Website verifiziert werden. Nur bestanden melden, wenn Plugin-, Hosting-, API- oder Server-Evidenz vorhanden ist. Ein vorhandenes Backup ist nicht automatisch ein getestetes Restore.

## Recht/DSGVO

Automatisch kann nur die technische Präsenz/Erreichbarkeit von Impressum und Datenschutzerklärung geprüft werden. Keine Rechtskonformität behaupten. Dr.-DSGVO- oder andere externe Legal-Scanner nur nutzen, wenn automatisierbar und ohne Umgehung von Captchas/Schutzmaßnahmen.

## Visuelle Prüfung

Playwright erzeugt Desktop-, Mobile- und Tablet-Screenshots und prüft horizontalen Overflow. Danach muss der Agent die Screenshots auf Überlagerungen, abgeschnittene Inhalte, fehlende Navigation, kaputte Bilder und deutliche Layoutfehler ansehen. Bei vorhandenen akzeptierten Baselines können Screenshot-Diffs ergänzt werden.

## Bericht

Der Bericht nutzt das mitgelieferte Word-Template. Probleme und nicht verifizierbare Punkte werden zusätzlich unter `Hinweise / Feststellungen` aufgeführt. Keine Credentials oder Tokens in Bericht, JSON oder Screenshots aufnehmen.
