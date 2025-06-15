from PySide6.QtCore import QObject, Signal

from ..components.dashboard_navitem import DashboardNavItem
from ..config.constants import ASSET_MAP

import typing
if typing.TYPE_CHECKING:
    from ..views.dashboard import DashboardView
    from ..models.user import User


class DashboardController(QObject):
    on_sign_out = Signal()

    def __init__(self, view: "DashboardView", user: "User") -> None:
        super().__init__()
        self.view = view
        self.user = user
        self.current_tab: str | None = None
        self.nav_tabs: dict[str, DashboardNavItem] = {}

    def setup_connections(self) -> None:
        self.setup_navigation(self.user.role)
        nav_layout = self.view.navigation_panel.layout()
        nav_layout.addStretch()
        self.append_navigation_item(
            ASSET_MAP['log-out'], "Sign out", "sign-out",
        )

    def append_navigation_item(
        self,
        icon_path: str,
        label: str,
        ref: str,
    ) -> None:
        layout = self.view.navigation_panel.layout()
        item = DashboardNavItem(
            icon_path,
            label,
            parent=self.view.navigation_panel
        )
        item.clicked.connect(lambda: self.select_tab(ref))
        item.setProperty("nav-name", ref)
        self.nav_tabs[ref] = item
        layout.addWidget(item)

    def tab_sign_out(self) -> None:
        self.on_sign_out.emit()
        
    def select_tab(self, nav_ref: str) -> None:
        if nav_ref == self.current_tab:
            return
        if nav_ref == "sign-out":
            self.tab_sign_out()
            return
        self.select_nav_item(nav_ref)
        self.current_tab = nav_ref

    def select_nav_item(self, which: str) -> None:
        if self.current_tab is not None:
            self.nav_tabs[self.current_tab].set_selected(False)
        self.nav_tabs[which].set_selected(True)

    def setup_navigation(self, role: str) -> None:
        match role:
            case "customer":
                which_nav_items = self.view.CUSTOMER_NAV_ITEMS
                which_tab = "orders"
            case "service-provider":
                which_nav_items = self.view.SERVICE_PROVIDER_NAV_ITEMS
                which_tab = "dashboard"
            case _:
                raise RuntimeError(f"Invalid user role: {role!r}")
        for item_params in which_nav_items:
            self.append_navigation_item(*item_params)
        self.select_tab(which_tab)