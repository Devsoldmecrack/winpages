import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt

from theme import apply_dark_palette
from ui.home import HomeWindow
from utils.paths import asset_path


def main():
    # Ensure proper taskbar grouping and icon on Windows
    if os.name == 'nt':
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("WinPages.Devsoldmecrack")
        except Exception:
            pass
    app = QApplication(sys.argv)
    # Set app icon (prefer .ico on Windows taskbar)
    svg_path = asset_path("assets", "app_icon.svg")
    ico_path = asset_path("assets", "app_icon.ico")
    if os.name == 'nt':
        try:
            if not os.path.exists(ico_path) and os.path.exists(svg_path):
                # Render SVG to 256x256 and save as ICO for Windows
                renderer = QSvgRenderer(svg_path)
                pm = QPixmap(256, 256)
                pm.fill(Qt.transparent)
                from PySide6.QtGui import QPainter
                p = QPainter(pm)
                renderer.render(p)
                p.end()
                pm.save(ico_path, "ICO")
            if os.path.exists(ico_path):
                app.setWindowIcon(QIcon(ico_path))
            else:
                app.setWindowIcon(QIcon(svg_path))
        except Exception:
            app.setWindowIcon(QIcon(svg_path))
    else:
        app.setWindowIcon(QIcon(svg_path))
    apply_dark_palette(app)
    w = HomeWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
