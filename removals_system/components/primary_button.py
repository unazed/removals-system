from PySide6.QtWidgets import QPushButton


class PrimaryButton(QPushButton):
    def __init__(self, text: str, parent=None) -> None:
        super().__init__(text, parent)
        self.setFixedHeight(35)
        self.setStyleSheet("""
            QPushButton {
                background-color: #89a69f;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #779589;
            }
        """)