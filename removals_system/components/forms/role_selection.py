from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt

from ...controllers.role_selection import RoleSelectionController
from ...config.constants import ASSET_MAP


class RoleSelectionForm(QWidget):
    def __init__(
        self,
        title: str,
        body: QWidget,
        footer: QWidget | None = None
    ) -> None:
        super().__init__()
        self.setStyleSheet("""
            QFrame#line {
                background-color: #e0e0e0;
                max-height: 1px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.addStretch()

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Albert Sans", 20))
        title_label.setTextFormat(Qt.RichText)
        layout.addWidget(title_label)
        layout.addSpacing(10)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setObjectName("line")
        divider.setFixedWidth(400)
        divider.setStyleSheet("QFrame { color: #dadada; }")
        layout.addWidget(divider, alignment=Qt.AlignCenter)
        layout.addSpacing(40)

        layout.addWidget(body)

        if footer is not None:
            layout.addWidget(footer)

        layout.addSpacing(40)
        layout.addStretch()

        logo_label = QLabel()
        logo_pixmap = QPixmap(ASSET_MAP['logo-black'])
        logo_label.setPixmap(
            logo_pixmap.scaled(
                70, 30,
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
