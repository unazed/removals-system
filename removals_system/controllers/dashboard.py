from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt

from ..components.dashboard_navitem import DashboardNavItem
from ..config.constants import ASSET_MAP

import typing
if typing.TYPE_CHECKING:
    from ..views.dashboard import DashboardView
    from ..models.user import User


class DashboardController:
    def __init__(self, view: "DashboardView", user: "User") -> None:
        self.view = view
        self.user = user

    def setup_connections(self) -> None:
        if self.user.role == "customer":
            self.populate_customer_navigation()
        elif self.user.role == "service-provider":
            self.populate_service_provider_navigation()
        nav_layout = self.view.navigation_panel.layout()
        nav_layout.addStretch()
        self.append_navigation_item(
            ASSET_MAP['log-out'], "Sign out", "sign-out",
            has_underline=False
        )
    
    def append_navigation_item(
        self,
        icon_path: str,
        label: str,
        ref: str,
        *,
        has_underline: bool = False
    ) -> None:
        layout = self.view.navigation_panel.layout()
        item = DashboardNavItem(
            icon_path,
            label,
            parent=self.view.navigation_panel
        )
        item.setProperty("nav-name", ref)
        layout.addWidget(item)

        if has_underline:
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Plain)
            line.setStyleSheet("color: #ccc;")
            layout.addWidget(line)

    def populate_customer_navigation(self) -> None:
        for item_params in self.view.CUSTOMER_NAV_ITEMS:
            self.append_navigation_item(*item_params)

    def populate_service_provider_navigation(self) -> None:
        pass