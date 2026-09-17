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

Dann `config.yaml` pro Kunde anpassen. Den Audit aus dem geöffneten Workspace-Ordner starten:

```bash
~/.agents/skills/website-maintenance-audit/scripts/run_audit.sh \
	~/.agents/skills/website-maintenance-audit/config.yaml
```

`run_audit.sh` verwendet automatisch `.venv/bin/python3`, wenn die lokale virtuelle Umgebung vorhanden ist. Eine Aktivierung der venv oder ein `PATH`-Prefix ist für den Auditlauf nicht erforderlich.

Ergebnisse landen standardmäßig unter `reports/<timestamp>/` im aktuellen Aufrufverzeichnis. Mit `AUDIT_OUTPUT_DIR=/pfad/zum/ziel` kann ein anderes Zielverzeichnis gesetzt werden.

## Was ohne Login läuft

Links, interne Seiten, Impressum/Datenschutz-Präsenz, HTML-basierter Google-Fonts-Check, SSL und Playwright-Screenshots. WordPress-Erkennung ist Best Effort.

## Was typischerweise Login/API/SSH braucht

Zuverlässige PHP-Version, zuverlässige WordPress-Version, Plugin-/Theme-Update-Status, Site Health und Backup-Nachweis.
