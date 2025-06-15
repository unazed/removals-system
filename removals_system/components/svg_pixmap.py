from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPainter, QPixmap, QColor
from PySide6.QtCore import Qt, QSize


class SVGPixmap:
    def __init__(self, path: str, size: QSize = QSize(24, 24)):
        self.renderer = QSvgRenderer(path)
        self.size = size

    def colored(self, color: QColor) -> QPixmap:
        pixmap = QPixmap(self.size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        self.renderer.render(painter)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()

        return pixmap