from PySide6.QtWidgets import QWidget, QLabel

from ..models.user import User


class Dashboard(QWidget):
    def __init__(self, user: User) -> None:
        super().__init__()
        self.user = user

        self.label = QLabel("woohooo", parent=self)