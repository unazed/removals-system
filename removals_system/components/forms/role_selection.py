from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QLabel
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt

from ...config.constants import ASSET_MAP

from ..form_widget import FormWidget

from typing import final, TYPE_CHECKING
if TYPE_CHECKING:
    from PySide6.QtGui import QResizeEvent


@final
class RoleSelectionForm(QWidget):
    def __init__(
        self,
        title: str,
        body: FormWidget,
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

        self.title_container = QWidget()
        self.title_container.setFixedWidth(int(self.width() * 0.6))
        title_layout = QVBoxLayout(self.title_container)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Albert Sans", 20))
        title_label.setTextFormat(Qt.RichText)
        # title_label.setScaledContents(True)
        title_label.setWordWrap(True)

        title_layout.addWidget(title_label)
        title_layout.addSpacing(10)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setObjectName("line")
        divider.setFixedWidth(400)
        divider.setStyleSheet("QFrame { color: #dadada; }")

        title_layout.addWidget(divider, alignment=Qt.AlignCenter)

        layout.addWidget(self.title_container, alignment=Qt.AlignCenter)
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

    def resizeEvent(self, event: "QResizeEvent"):
        super().resizeEvent(event)
        new_width = int(event.size().width() * 0.6)
        self.title_container.setFixedWidth(new_width)
