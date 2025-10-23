from PySide6.QtWidgets import QMainWindow, QTextEdit, QFileDialog, QToolBar, QColorDialog, QFontComboBox, QComboBox, QMessageBox
from PySide6.QtGui import QIcon, QTextCharFormat, QFont, QTextListFormat, QKeySequence, QAction, QTextCursor
from PySide6.QtCore import Qt, QFileInfo, QSize, Signal
import os

from utils.document_store import touch_recent, unique_path
from utils.thumbnails import ensure_thumbnail_for_file, ensure_thumbnail_for_content, thumb_path
from theme import EDITOR_TOOLBAR_QSS
from utils.paths import asset_path


class EditorWindow(QMainWindow):
    document_saved = Signal(str)
    def __init__(self, path: str | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("WinPages – Editor")
        self.resize(1100, 800)

        self.text = QTextEdit()
        self.text.setAcceptRichText(True)
        self.setCentralWidget(self.text)

        self._path = None
        self._build_toolbar()
        if path:
            self.open_file(path)

    def _build_toolbar(self):
        tb = QToolBar("Format")
        tb.setMovable(False)
        tb.setIconSize(QSize(18, 18))
        tb.setStyleSheet(EDITOR_TOOLBAR_QSS)
        self.addToolBar(tb)

        act_new = QAction(QIcon(self._icon_path("new.svg")), "New", self)
        act_new.triggered.connect(self.new_document)
        tb.addAction(act_new)

        act_open = QAction(QIcon(self._icon_path("open.svg")), "Open", self)
        act_open.setShortcut(QKeySequence.Open)
        act_open.triggered.connect(self.open_dialog)
        tb.addAction(act_open)

        act_save = QAction(QIcon(self._icon_path("save.svg")), "Save", self)
        act_save.setShortcut(QKeySequence.Save)
        act_save.triggered.connect(self.save)
        tb.addAction(act_save)

        tb.addSeparator()

        self.font_family = QFontComboBox()
        self.font_family.currentFontChanged.connect(self._apply_font_family)
        tb.addWidget(self.font_family)

        self.font_size = QComboBox()
        for s in [10, 12, 14, 16, 18, 20, 24, 28, 32, 36]:
            self.font_size.addItem(str(s), s)
        self.font_size.currentIndexChanged.connect(self._apply_font_size)
        tb.addWidget(self.font_size)
        self.font_size.setCurrentIndex(2)
        self._apply_font_size()

        act_bold = QAction(QIcon(self._icon_path("bold.svg")), "Bold", self)
        act_bold.setShortcut(QKeySequence.Bold)
        act_bold.setCheckable(True)
        act_bold.triggered.connect(lambda: self._toggle_weight(QFont.Bold))
        tb.addAction(act_bold)

        act_italic = QAction(QIcon(self._icon_path("italic.svg")), "Italic", self)
        act_italic.setShortcut(QKeySequence.Italic)
        act_italic.setCheckable(True)
        act_italic.triggered.connect(self._toggle_italic)
        tb.addAction(act_italic)

        act_underline = QAction(QIcon(self._icon_path("underline.svg")), "Underline", self)
        act_underline.setShortcut(QKeySequence.Underline)
        act_underline.setCheckable(True)
        act_underline.triggered.connect(self._toggle_underline)
        tb.addAction(act_underline)

        tb.addSeparator()

        act_bullets = QAction(QIcon(self._icon_path("bullet.svg")), "Bulleted List", self)
        act_bullets.triggered.connect(self._toggle_bullets)
        tb.addAction(act_bullets)

        act_num = QAction(QIcon(self._icon_path("number.svg")), "Numbered List", self)
        act_num.triggered.connect(self._toggle_numbers)
        tb.addAction(act_num)

        tb.addSeparator()

        act_color = QAction(QIcon(self._icon_path("color.svg")), "Color", self)
        act_color.triggered.connect(self._choose_color)
        tb.addAction(act_color)

        act_left = QAction(QIcon(self._icon_path("align-left.svg")), "Left", self)
        act_left.triggered.connect(lambda: self._set_align(Qt.AlignLeft))
        tb.addAction(act_left)

        act_center = QAction(QIcon(self._icon_path("align-center.svg")), "Center", self)
        act_center.triggered.connect(lambda: self._set_align(Qt.AlignHCenter))
        tb.addAction(act_center)

        act_right = QAction(QIcon(self._icon_path("align-right.svg")), "Right", self)
        act_right.triggered.connect(lambda: self._set_align(Qt.AlignRight))
        tb.addAction(act_right)

        tb.addSeparator()

        act_export = QAction(QIcon(self._icon_path("pdf.svg")), "Export PDF", self)
        act_export.triggered.connect(self.export_pdf)
        tb.addAction(act_export)

    def _icon_path(self, name: str) -> str:
        return asset_path("assets", "icons", name)

    def load_from_template(self, path: str):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                data = f.read()
            ext = QFileInfo(path).suffix().lower()
            if ext in ("html", "htm"):
                self.text.setHtml(data)
            else:
                self.text.setPlainText(data)
            # Do not bind to template file path
            self._path = None
            self.setWindowTitle("Untitled – WinPages")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _merge_format_on_selection(self, fmt: QTextCharFormat):
        cursor = self.text.textCursor()
        if not cursor.hasSelection():
            # Select the word under cursor when there's no selection; if document is empty, skip
            if not self.text.document().isEmpty():
                cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(fmt)
        self.text.mergeCurrentCharFormat(fmt)

    def _apply_font_family(self, f: QFont):
        fmt = QTextCharFormat()
        fmt.setFontFamily(f.family())
        self._merge_format_on_selection(fmt)

    def _apply_font_size(self):
        size = int(self.font_size.currentData())
        fmt = QTextCharFormat()
        fmt.setFontPointSize(size)
        self._merge_format_on_selection(fmt)

    def _toggle_weight(self, weight):
        fmt = QTextCharFormat()
        fmt.setFontWeight(weight if self.text.fontWeight() != weight else QFont.Normal)
        self._merge_format_on_selection(fmt)

    def _toggle_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(not self.text.fontItalic())
        self._merge_format_on_selection(fmt)

    def _toggle_underline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(not self.text.fontUnderline())
        self._merge_format_on_selection(fmt)

    def _toggle_bullets(self):
        cursor = self.text.textCursor()
        fmt = QTextListFormat()
        fmt.setStyle(QTextListFormat.ListDisc)
        cursor.createList(fmt)

    def _toggle_numbers(self):
        cursor = self.text.textCursor()
        fmt = QTextListFormat()
        fmt.setStyle(QTextListFormat.ListDecimal)
        cursor.createList(fmt)

    def _set_align(self, align):
        self.text.setAlignment(align)

    def _choose_color(self):
        c = QColorDialog.getColor(parent=self)
        if c.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(c)
            self._merge_format_on_selection(fmt)

    def new_document(self):
        self.text.clear()
        self._path = None
        self.setWindowTitle("Untitled – WinPages")

    def open_dialog(self):
        fn, _ = QFileDialog.getOpenFileName(self, "Open Document", os.path.expanduser("~"), "Documents (*.html *.htm *.rtf *.txt);;All Files (*.*)")
        if fn:
            self.open_file(fn)

    def open_file(self, path: str):
        self._path = path
        ext = QFileInfo(path).suffix().lower()
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                data = f.read()
            if ext in ("html", "htm"):
                self.text.setHtml(data)
            else:
                self.text.setPlainText(data)
            self.setWindowTitle(f"{os.path.basename(path)} – WinPages")
            touch_recent(path)
            ensure_thumbnail_for_file(path)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def save(self):
        if not self._path:
            # Auto-save new docs into app documents folder with a unique name
            suggested = unique_path("Document.html")
            self._path = suggested
            ok = self._save_to(self._path)
            if ok:
                self.document_saved.emit(self._path)
            return ok
        ok = self._save_to(self._path)
        if ok:
            self.document_saved.emit(self._path)
        return ok

    def save_as(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Save As", self._path or os.path.expanduser("~"), "HTML (*.html);;RTF (*.rtf);;Text (*.txt)")
        if fn:
            self._path = fn
            ok = self._save_to(fn)
            if ok:
                self.document_saved.emit(fn)
            return ok

    def _save_to(self, path: str):
        ext = QFileInfo(path).suffix().lower()
        try:
            if ext == "html":
                data = self.text.toHtml()
            elif ext == "rtf":
                data = self.text.toHtml()
            else:
                data = self.text.toPlainText()
            with open(path, "w", encoding="utf-8") as f:
                f.write(data)
            self.setWindowTitle(f"{os.path.basename(path)} – WinPages")
            touch_recent(path)
            is_html = ext in ("html", "htm", "rtf")
            ensure_thumbnail_for_content(data, is_html, thumb_path(path))
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return False

    def export_pdf(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Export as PDF", os.path.expanduser("~"), "PDF (*.pdf)")
        if not fn:
            return
        try:
            from PySide6.QtGui import QPageLayout, QPageSize, QTextDocument
            from PySide6.QtPrintSupport import QPrinter
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            printer.setPageSize(QPrinter.A4)
            doc = self.text.document()
            doc.print_(printer)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
