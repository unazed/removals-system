from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtGui import (
    QPixmap, QMouseEvent, QColor, QPalette, QFontMetrics, QFont
)
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

        self.base_icon_color = icon_color
        self.icon_label = QLabel()
        self.svg_icon = SVGPixmap(icon_path)
        self.icon_label.setPixmap(self.svg_icon.colored(
            QColor(icon_color)
        ).scaled(
            24, 24,
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        layout.addWidget(self.icon_label)

        self.text_label = QLabel(label)
        self.text_label.setStyleSheet(f"""
            QLabel {{
                color: {self.TEXT_COLOR};
                font-size: 16px;
            }}

            QLabel[selected="true"] {{
                color: black;
            }}
        """)
        layout.addWidget(self.text_label)
        layout.addStretch()

        self._adjust_label_width()
        self.set_selected(False)

    def _adjust_label_width(self) -> None:
        bold_font = QFont(self.text_label.font())
        bold_font.setBold(True)
        bold_metrics = QFontMetrics(bold_font)
        bold_width = bold_metrics.horizontalAdvance(self.text_label.text())
        self.text_label.setFixedWidth(bold_width)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    def set_selected(self, selected: bool):
        self._selected = selected
        self.icon_label.setPixmap(self.svg_icon.colored(
            QColor("#000") if selected else self.base_icon_color
        ))
        self.text_label.setProperty(
            "selected",
            "true" if selected else "false"
        )
        self.text_label.style().unpolish(self.text_label)
        self.text_label.style().polish(self.text_label)

    def is_selected(self):
        return self._selected
