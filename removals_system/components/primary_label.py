from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class PrimaryLabel(QLabel):
    def __init__(self, text: str, parent=None) -> None:
        super().__init__(text, parent)
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignCenter)
        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(False)
        self.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #444;
            }
            a {
                text-decoration: none;
            }
        """)