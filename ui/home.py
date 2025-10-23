from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea, QGridLayout, QLineEdit, QGraphicsDropShadowEffect, QFileDialog, QDialog, QMenu, QInputDialog
from PySide6.QtCore import Qt, QSize, QUrl, QTimer
from PySide6.QtGui import QPainter, QFont, QPixmap, QColor, QDesktopServices
import os
import subprocess

from ui.editor import EditorWindow
from utils.document_store import list_recents, import_file, touch_recent, remove_recent
from theme import PRIMARY_BUTTON_QSS, CARD_QSS, SHEET_QSS, SEARCH_QSS, MENU_QSS
from ui.templates import TemplatePicker
from utils.thumbnails import ensure_thumbnail_for_file, thumb_path


class GradientWidget(QWidget):
    def paintEvent(self, e):
        from theme import gradient_background
        p = QPainter(self)
        p.fillRect(self.rect(), gradient_background(self))


class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WinPages")
        self.resize(1100, 800)
        self.setAcceptDrops(True)

        root = GradientWidget()
        self.setCentralWidget(root)
        v = QVBoxLayout(root)
        v.setContentsMargins(32, 24, 32, 24)
        v.setSpacing(16)

        hero = QFrame()
        hero.setFixedHeight(260)
        hero.setStyleSheet(CARD_QSS)
        hv = QVBoxLayout(hero)
        hv.setAlignment(Qt.AlignCenter)

        shadow_hero = QGraphicsDropShadowEffect(self)
        shadow_hero.setBlurRadius(40)
        shadow_hero.setOffset(0, 12)
        shadow_hero.setColor(QColor(0, 0, 0, 160))
        hero.setGraphicsEffect(shadow_hero)

        title = QLabel("Pages")
        f = QFont()
        f.setPointSize(44)
        f.setWeight(QFont.ExtraBold)
        title.setFont(f)
        title.setStyleSheet("color: white")
        hv.addWidget(title, 0, Qt.AlignHCenter)

        btn = QPushButton("Jetzt schreiben")
        btn.setStyleSheet(PRIMARY_BUTTON_QSS)
        btn.clicked.connect(self.open_editor)
        hv.addWidget(btn, 0, Qt.AlignHCenter)

        sub = QPushButton("Vorlage auswählen")
        sub.setFlat(True)
        sub.setStyleSheet("color: rgb(150, 170, 200); font-weight: 600;")
        sub.clicked.connect(self.open_templates)
        hv.addWidget(sub, 0, Qt.AlignHCenter)

        copyright_lbl = QLabel("© Devsoldmecrack")
        copyright_lbl.setStyleSheet("color: rgb(150, 150, 160); font-size: 11px;")
        hv.addWidget(copyright_lbl, 0, Qt.AlignHCenter)

        v.addWidget(hero)

        sheet = QFrame()
        sheet.setStyleSheet(SHEET_QSS)
        sv = QVBoxLayout(sheet)
        sv.setContentsMargins(16, 16, 16, 16)
        sv.setSpacing(12)

        shadow_sheet = QGraphicsDropShadowEffect(self)
        shadow_sheet.setBlurRadius(50)
        shadow_sheet.setOffset(0, 18)
        shadow_sheet.setColor(QColor(0, 0, 0, 180))
        sheet.setGraphicsEffect(shadow_sheet)

        top = QHBoxLayout()
        search = QLineEdit()
        search.setPlaceholderText("Suchen…")
        search.setStyleSheet(SEARCH_QSS)
        # debounce: 200ms after typing stops
        self._searchTimer = QTimer(self)
        self._searchTimer.setSingleShot(True)
        self._searchTimer.setInterval(200)
        search.textChanged.connect(lambda _: self._searchTimer.start())
        self._searchTimer.timeout.connect(self.refresh)
        top.addWidget(search)
        import_btn = QPushButton("Importieren")
        import_btn.clicked.connect(self.import_files)
        top.addWidget(import_btn)
        sv.addLayout(top)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        self.grid = QGridLayout(container)
        self.grid.setHorizontalSpacing(24)
        self.grid.setVerticalSpacing(18)
        scroll.setWidget(container)
        sv.addWidget(scroll)

        v.addWidget(sheet, 1)

        self._search = search
        self.refresh()

    def import_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Dateien importieren", str(os.path.expanduser("~")), "Dokumente (*.html *.htm *.rtf *.txt);;Alle Dateien (*.*)")
        changed = False
        for f in files:
            try:
                dest = import_file(f)
                ensure_thumbnail_for_file(dest)
                changed = True
            except Exception:
                pass
        if changed:
            self.refresh()

    def open_editor(self):
        w = EditorWindow(parent=self)
        w.document_saved.connect(lambda _: self.refresh())
        w.show()

    def open_templates(self):
        dlg = TemplatePicker(self)
        if dlg.exec() == QDialog.Accepted:
            path = dlg.selected_path()
            if path:
                w = EditorWindow(parent=self)
                w.document_saved.connect(lambda _: self.refresh())
                w.load_from_template(path)
                w.show()

    def refresh(self):
        rec = [r for r in list_recents() if self._search.text().lower() in r.get("name", "").lower()]
        while self.grid.count():
            item = self.grid.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        for i, r in enumerate(rec[:30]):
            card = self._doc_card(r)
            self.grid.addWidget(card, i // 4, i % 4)

    def _doc_card(self, r):
        f = QFrame()
        f.setStyleSheet(CARD_QSS)
        f.setFixedSize(QSize(210, 260))
        v = QVBoxLayout(f)
        v.setContentsMargins(12, 12, 12, 12)
        v.setSpacing(8)

        preview = QLabel()
        preview.setAlignment(Qt.AlignCenter)
        preview.setFixedHeight(160)
        # Try load or build thumbnail
        path = r.get("path")
        thumb = None
        if path:
            thumb = ensure_thumbnail_for_file(path) or (thumb_path(path) if path else None)
        if thumb and QPixmap(thumb).isNull() is False:
            pm = QPixmap(thumb).scaled(180, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            preview.setPixmap(pm)
        else:
            preview.setText("📝")
        v.addWidget(preview)

        name = QLabel(r.get("name"))
        name.setStyleSheet("color: white; font-weight: 600")
        v.addWidget(name)

        meta = QLabel(f"{r.get('ts','')} · {int(r.get('size',0)/1024)} KB")
        meta.setStyleSheet("color: rgb(200,200,200)")
        v.addWidget(meta)

        def on_mouse_release(e):
            if e.button() == Qt.LeftButton:
                self.open_path(r.get("path"))
            else:
                e.ignore()
        f.mouseReleaseEvent = on_mouse_release
        # context menu for rename/reveal
        f._doc_path = r.get("path")
        def context_menu(event):
            menu = QMenu(f)
            menu.setStyleSheet(MENU_QSS)
            act_open = menu.addAction("Öffnen")
            act_rename = menu.addAction("Umbenennen…")
            act_reveal = menu.addAction("Im Explorer anzeigen")
            chosen = menu.exec(event.globalPos())
            if chosen == act_open:
                self.open_path(f._doc_path)
            elif chosen == act_rename:
                self._rename_document(f._doc_path)
            elif chosen == act_reveal:
                self._reveal_in_explorer(f._doc_path)
        f.contextMenuEvent = context_menu
        return f

    def open_path(self, path: str):
        w = EditorWindow(path=path, parent=self)
        w.document_saved.connect(lambda _: self.refresh())
        w.show()

    def _reveal_in_explorer(self, path: str):
        if os.name == 'nt':
            try:
                subprocess.run(["explorer", "/select,", path])
            except Exception:
                QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(path)))
        else:
            QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(path)))

    def _unique_name_in_dir(self, directory: str, base_name: str) -> str:
        name, ext = os.path.splitext(base_name)
        candidate = os.path.join(directory, f"{name}{ext}")
        i = 1
        while os.path.exists(candidate):
            candidate = os.path.join(directory, f"{name} {i}{ext}")
            i += 1
        return candidate

    def _rename_document(self, path: str):
        if not path or not os.path.exists(path):
            return
        base = os.path.basename(path)
        new_name, ok = QInputDialog.getText(self, "Umbenennen", "Neuer Name:", text=base)
        if not ok or not new_name.strip():
            return
        # Keep extension if user removed it accidentally
        if not os.path.splitext(new_name)[1]:
            new_name += os.path.splitext(base)[1]
        dest = self._unique_name_in_dir(os.path.dirname(path), new_name)
        try:
            old_thumb = thumb_path(path)
            os.replace(path, dest)
            # Update recents and thumbnail
            remove_recent(path)
            touch_recent(dest)
            ensure_thumbnail_for_file(dest)
            if os.path.exists(old_thumb) and old_thumb != thumb_path(dest):
                try:
                    os.remove(old_thumb)
                except Exception:
                    pass
            self.refresh()
        except Exception:
            pass

    # Drag & Drop from Explorer into window
    def dragEnterEvent(self, event):
        md = event.mimeData()
        if md.hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        md = event.mimeData()
        changed = False
        if md.hasUrls():
            for url in md.urls():
                local = url.toLocalFile()
                if local and os.path.isfile(local):
                    try:
                        dest = import_file(local)
                        ensure_thumbnail_for_file(dest)
                        changed = True
                    except Exception:
                        pass
        if changed:
            self.refresh()
