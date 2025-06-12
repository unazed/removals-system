from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap, QMouseEvent, QColor, QPalette
from PySide6.QtCore import Signal, Qt

from .svg_pixmap import SVGPixmap


class DashboardNavItem(QWidget):
    DEFAULT_BG = "#89A7A0"
    SELECTED_BG = "#6E8C85"
    TEXT_COLOR = "white"

    clicked = Signal()

    def __init__(
        self,
        icon_path: str,
        label: str,
        icon_color: QColor = QColor("#fff"),
        parent=None
    ) -> None:
        super().__init__(parent=parent)

        self._selected = False

        self.setFixedHeight(60)
        self.setCursor(Qt.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 25, 0)
        layout.setSpacing(15)

        self.icon_label = QLabel()
        pixmap = SVGPixmap(icon_path)
        pixmap.set_color(icon_color)
        self.icon_label.setPixmap(pixmap.scaled(
            24, 24,
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        layout.addWidget(self.icon_label)

        self.text_label = QLabel(label)
        self.text_label.setStyleSheet(f"color: {self.TEXT_COLOR}; font-size: 16px;")
        layout.addWidget(self.text_label)

        layout.addStretch()

        self.set_selected(False)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    def set_selected(self, selected: bool):
        self._selected = selected
        palette = self.palette()
        bg_color = self.SELECTED_BG if selected else self.DEFAULT_BG
        palette.setColor(QPalette.Window, QColor(bg_color))
        self.setPalette(palette)

    def is_selected(self):
        return self._selected
