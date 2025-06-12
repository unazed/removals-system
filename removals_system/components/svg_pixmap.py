from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPainter, QPixmap, QColor
from PySide6.QtCore import Qt, QSize


class SVGPixmap(QPixmap):
    def __init__(self, path: str, size: QSize = QSize(24, 24)):
        super().__init__(size)
        self.renderer = QSvgRenderer(path)

    def set_color(self, color: QColor):
        self.fill(Qt.transparent)
        painter = QPainter(self)
        self.renderer.render(painter)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(self.rect(), color)
        painter.end()
