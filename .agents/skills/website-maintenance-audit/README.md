# Globaler Website-Wartungs-Audit Skill

Empfohlene Installation in Dotfiles:

```bash
mkdir -p ~/dotfiles/agents/skills
cp -r website-maintenance-audit ~/dotfiles/agents/skills/
mkdir -p ~/.agents/skills
ln -s ~/dotfiles/agents/skills/website-maintenance-audit ~/.agents/skills/website-maintenance-audit
```

Alternativ kann `~/.agents/skills` insgesamt auf den Dotfiles-Ordner verlinkt werden.

## Setup

```bash
cd ~/.agents/skills/website-maintenance-audit
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp config.example.yaml config.yaml
```

Dann `config.yaml` pro Kunde anpassen und ausführen:

```bash
./scripts/run_audit.sh config.yaml
```

Ergebnisse landen unter `reports/<timestamp>/`.

## Was ohne Login läuft

Links, interne Seiten, Impressum/Datenschutz-Präsenz, HTML-basierter Google-Fonts-Check, SSL und Playwright-Screenshots. WordPress-Erkennung ist Best Effort.

## Was typischerweise Login/API/SSH braucht

Zuverlässige PHP-Version, zuverlässige WordPress-Version, Plugin-/Theme-Update-Status, Site Health und Backup-Nachweis.
