# WinPages

Elegantes, modulares Schreib-Tool (ähnlich Apple Pages) mit PySide6. Fokus auf UX, RichText, Vorlagen, Verlauf mit Vorschaubildern und einem dunklen Blau/Grau-Theme.

## Features
- Startscreen mit Hero-Card, Vorlagen-Picker und Verlauf (mit Thumbnails)
- Editor mit RichText (`QTextEdit`): Schrift, Größe, Fett/Kursiv/Unterstr., Listen, Ausrichtung, Textfarbe
- Dateioperationen: Neu, Öffnen, Speichern, Speichern unter, Export als PDF
- Auto-Speichern für neue Dokumente in `~/.winpages/documents/` mit eindeutigem Namen
- Verlaufsspeicher in `~/.winpages/recents.json` + Thumbnail-Cache in `~/.winpages/thumbs/`
- Importieren-Button und Drag&Drop vom Explorer auf die Startseite
- Kontextmenü auf Dokument-Karten: Öffnen, Umbenennen, Im Explorer anzeigen
- Dunkles Blau/Grau-Theme, 3D-Schatten, SVG-Toolbar-Icons

## Projektstruktur
```
WinPages/
  assets/
    app_icon.svg
    icons/*.svg
  templates/
    Notiz.html
  ui/
    home.py
    editor.py
    templates.py
  utils/
    document_store.py
    thumbnails.py
  theme.py
  main.py
  requirements.txt
```

## Lokale Entwicklung
```bash
pip install -r requirements.txt
python main.py
```

## Build (Windows, Portable EXE)
Wir nutzen PyInstaller. Die GitHub Action erzeugt automatisch eine portable EXE und ein ZIP der `dist/`-Ausgabe.

Manuell lokal:
```bash
pip install pyinstaller
# (optional) ICO aus SVG generieren – die Action erledigt das automatisch
python tools/generate_ico.py

pyinstaller ^
  --noconfirm --windowed ^
  --name WinPages ^
  --icon assets/app_icon.ico ^
  --add-data "assets;assets" ^
  --add-data "templates;templates" ^
  main.py
```
Die EXE liegt dann unter `dist/WinPages/WinPages.exe`.

## CI/CD
- Workflow: `.github/workflows/build.yml`
  - Läuft auf `windows-latest`
  - Installiert Abhängigkeiten
  - Generiert `assets/app_icon.ico` aus `assets/app_icon.svg`
  - Baut mit PyInstaller
  - Lädt Artefakte hoch: `WinPages.exe` + `WinPages.zip`

## Installer (optional)
Für einen klassischen Windows-Installer (Startmenü, Deinstallations-Eintrag) kannst du Inno Setup verwenden. Eine Beispiel-`InnoSetup.iss` kann später ergänzt werden; die Action kann dann `iscc` aufrufen und das `.exe`-Setup als Artefakt hochladen.

## Repo-Name-Vorschlag
- `winpages` oder `winpages-notes`

## Lizenz
Füge eine Lizenz hinzu (z. B. MIT), je nach Bedarf.
