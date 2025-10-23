import os
from PySide6.QtGui import QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt

BASE = os.path.dirname(os.path.dirname(__file__))
SVG = os.path.join(BASE, 'assets', 'app_icon.svg')
ICO = os.path.join(BASE, 'assets', 'app_icon.ico')

def main():
    if not os.path.exists(SVG):
        print('SVG not found:', SVG)
        return
    pm = QPixmap(256, 256)
    pm.fill(Qt.transparent)
    r = QSvgRenderer(SVG)
    p = QPainter(pm)
    r.render(p)
    p.end()
    pm.save(ICO, 'ICO')
    print('Saved', ICO)

if __name__ == '__main__':
    main()
