# WinPages

An elegant, modular writing tool (Pages-like) built with PySide6. Focus on UX, rich text, templates, recent documents with thumbnails, and a dark blue/gray theme.

## Features
- Start screen with hero card, template picker, and recents (with thumbnails)
- Rich text editor (`QTextEdit`): font family/size, bold/italic/underline, bulleted/numbered lists, alignment, text color
- File operations: New, Open, Save, Save As, Export as PDF
- Auto-save for new documents into `~/.winpages/documents/` with unique names
- Recents store in `~/.winpages/recents.json` + thumbnail cache in `~/.winpages/thumbs/`
- Import button and drag & drop from Explorer onto the home screen
- Card context menu: Open, Rename, Reveal in Explorer
- Dark blue/gray theme, 3D shadows, SVG toolbar icons

## Project structure
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

## Local development
```bash
pip install -r requirements.txt
python main.py
```

## Build (Windows, portable EXE)
We use PyInstaller. The GitHub Action builds a portable EXE and a zipped `dist/` output automatically.

Manual local build:
```bash
pip install pyinstaller
# (optional) generate ICO from SVG – CI does this automatically
python tools/generate_ico.py

pyinstaller ^
  --noconfirm --windowed ^
  --name WinPages ^
  --icon assets/app_icon.ico ^
  --hidden-import PySide6.QtSvg --collect-submodules PySide6 ^
  --add-data "assets;assets" ^
  --add-data "templates;templates" ^
  main.py
```
The EXE will be at `dist/WinPages/WinPages.exe`.

## CI/CD
- Workflow: `.github/workflows/build.yml`
  - Runs on `windows-latest`
  - Installs dependencies
  - Generates `assets/app_icon.ico` from `assets/app_icon.svg`
  - Builds with PyInstaller
  - Uploads artifacts: `WinPages.exe`, `WinPages-dist/`, and `WinPages.zip`

## Installer (optional)
For a classic Windows installer (Start Menu entry, uninstall), use Inno Setup. We can add a sample `InnoSetup.iss` and a CI step to run `iscc` and publish the installer.

## Repository name suggestion
- `winpages` or `winpages-notes`

## License
Add a license (e.g., MIT) as needed.
