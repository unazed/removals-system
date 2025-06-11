from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QLabel, QHBoxLayout
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt

from ...config.constants import ASSET_MAP

from ..form import Form

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from PySide6.QtGui import QResizeEvent


class RoleSelectionForm(QWidget):
    def __init__(
        self,
        title: str,
        body: Form,
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
        layout.setContentsMargins(100, 40, 100, 40)
        layout.addStretch()

        title_horizontal_container = QWidget()
        title_horizontal_layout = QHBoxLayout(title_horizontal_container)
        title_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        
        title_horizontal_layout.addStretch(2)
        
        self.title_container = QWidget()
        title_layout = QVBoxLayout(self.title_container)

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Albert Sans", 20))
        self.title_label.setTextFormat(Qt.RichText)
        self.title_label.setWordWrap(True)

        title_layout.addWidget(self.title_label)
        title_layout.addSpacing(10)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setObjectName("line")
        divider.setFixedWidth(400)
        divider.setStyleSheet("QFrame { color: #dadada; }")

        title_layout.addWidget(divider, alignment=Qt.AlignCenter)

        title_horizontal_layout.addWidget(self.title_container, 7)
        title_horizontal_layout.addStretch(2)

        layout.addWidget(title_horizontal_container)
        layout.addSpacing(40)

        self.body = body
        layout.addWidget(body)

        self.footer = footer
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