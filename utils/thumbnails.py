import os
from typing import Optional
from PySide6.QtGui import QTextDocument, QImage, QPainter, QColor
from PySide6.QtCore import QSize, QRectF, Qt

from .document_store import APP_DIR

THUMB_DIR = os.path.join(APP_DIR, "thumbs")
os.makedirs(THUMB_DIR, exist_ok=True)


def thumb_path(doc_path: str) -> str:
    base = os.path.basename(doc_path)
    name, _ = os.path.splitext(base)
    return os.path.join(THUMB_DIR, f"{name}.png")


def ensure_thumbnail_for_content(content: str, is_html: bool, out_path: str) -> Optional[str]:
    try:
        w, h = 210, 270
        img = QImage(w, h, QImage.Format_ARGB32)
        img.fill(QColor(255, 255, 255))

        doc = QTextDocument()
        if is_html:
            doc.setHtml(content)
        else:
            doc.setPlainText(content)
        doc.setTextWidth(160)

        p = QPainter(img)
        p.setRenderHint(QPainter.Antialiasing)
        # draw page shadow-ish border
        p.fillRect(10, 10, 190, 250, QColor(245, 246, 248))
        p.setPen(QColor(220, 220, 225))
        p.drawRect(10, 10, 190, 250)

        p.translate(20, 20)
        doc.drawContents(p, QRectF(0, 0, 170, 230))
        p.end()

        img.save(out_path)
        return out_path
    except Exception:
        return None


def ensure_thumbnail_for_file(path: str) -> Optional[str]:
    try:
        if not os.path.exists(path):
            return None
        out = thumb_path(path)
        # Rebuild if missing or older than source
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(path):
            return out
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
        is_html = os.path.splitext(path)[1].lower() in (".html", ".htm", ".rtf")
        return ensure_thumbnail_for_content(data, is_html, out)
    except Exception:
        return None
