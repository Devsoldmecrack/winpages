import os
from glob import glob
from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")

class TemplatePicker(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Vorlage auswählen")
        self.resize(520, 420)
        v = QVBoxLayout(self)

        self.list = QListWidget()
        v.addWidget(self.list, 1)

        btns = QHBoxLayout()
        self.ok = QPushButton("Verwenden")
        self.cancel = QPushButton("Abbrechen")
        self.ok.clicked.connect(self.accept)
        self.cancel.clicked.connect(self.reject)
        btns.addStretch(1)
        btns.addWidget(self.cancel)
        btns.addWidget(self.ok)
        v.addLayout(btns)

        os.makedirs(TEMPLATES_DIR, exist_ok=True)
        self._load()

    def _load(self):
        self.list.clear()
        for path in sorted(glob(os.path.join(TEMPLATES_DIR, "*.html")) + glob(os.path.join(TEMPLATES_DIR, "*.txt"))):
            item = QListWidgetItem(os.path.basename(path))
            item.setData(Qt.UserRole, path)
            self.list.addItem(item)

    def selected_path(self) -> str | None:
        it = self.list.currentItem()
        return it.data(Qt.UserRole) if it else None
