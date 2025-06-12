from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QLabel
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

from ..models.user import User
from ..controllers.dashboard import DashboardController

from ..config.constants import ASSET_MAP


class DashboardView(QWidget):
    CUSTOMER_NAV_ITEMS = (
        (ASSET_MAP['table-of-contents'], "My orders", "orders"),
        (ASSET_MAP['calendar-plus'], "Create order", "create-order"),
        (ASSET_MAP['hand-coins'], "View invoices", "invoices"),
        (ASSET_MAP['user'], "My details", "details")
    )

    SERVICE_PROVIDER_NAV_ITEMS = (
        (ASSET_MAP['table-of-contents'], "Dashboard", "dashboard"),
        (ASSET_MAP['calendar-plus'], "Market", "market"),
        (ASSET_MAP['hand-coins'], "View invoices", "invoices"),
        (ASSET_MAP['user'], "Business details", "details")
    )

    def __init__(self, user: User):
        super().__init__()

        self.setWindowTitle("Dashboard")
        self.controller = DashboardController(self, user)

        main_layout = QHBoxLayout(self)
        self.navigation_panel = self.create_navigation_panel()
        main_layout.addWidget(self.navigation_panel)

        self.stack = QStackedLayout()

        self.controller.setup_connections()

        container = QWidget()
        container.setLayout(self.stack)
        main_layout.addWidget(container, stretch=1)

    def create_navigation_panel(self) -> QWidget:
        panel = QWidget()
        panel.setStyleSheet("background-color: #89a69f;")
        panel.setFont(QFont("Albert Sans", 10))
        layout = QVBoxLayout(panel)
        layout.setSpacing(0)
        layout.addSpacing(20)

        image_label = QLabel()
        pixmap = QPixmap(ASSET_MAP['logo-white'])
        image_label.setPixmap(
            pixmap.scaled(
                70, 30,
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)
        layout.addSpacing(20)

        return panel