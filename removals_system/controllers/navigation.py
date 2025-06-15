from PySide6.QtWidgets import QMainWindow, QStackedWidget

from ..views.authentication import AuthenticationView
from ..views.role_selection import RoleSelectionView
from ..views.dashboard import DashboardView

from typing import TYPE_CHECKING
from functools import partial

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget
    from Pyside6.QtCore import Signal

    from ..controllers.authentication import AuthenticationController
    from ..controllers.dashboard import DashboardController
    from ..controllers.role_selection import RoleSelectionController


class NavigationController(QMainWindow):
    def __init__(self, default_view: str) -> None:
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.view_map = {
            "authentication": {
                "class": AuthenticationView,
                "instance": None,
                "reusable": True
            },
            "role_selection": {
                "class": RoleSelectionView,
                "instance": None,
                "reusable": True
            },
            "dashboard": {
                "class": DashboardView,
                "instance": None,
                "reusable": False
            }
        }

        self.show_view(default_view)

    def show_view(self, which_view: str, *args, **kwargs) -> None:
        if which_view not in self.view_map:
            raise ValueError(f"Unknown view requested: {which_view!r}")

        view_params = self.view_map[which_view]
        if (view_inst := view_params['instance']) is not None:
            if view_params['reusable']:
                self.stacked_widget.setCurrentWidget(view_inst)
                return
            self.clear_view_instance(which_view)
        
        view_inst = view_params['class'](*args, **kwargs)
        self._connect_view_signals(which_view, view_inst)
        view_params['instance'] = view_inst
        self.stacked_widget.addWidget(view_inst)
        self.stacked_widget.setCurrentWidget(view_inst)

    def _connect_signal(self, signal: "Signal", which_view: str) -> None:
        signal.connect(
            lambda *args, **kwargs: self.show_view(which_view, *args, **kwargs)
        )

    def _connect_view_signals(self, which_view: str, view: "QWidget") -> None:
        match which_view:
            case "authentication":
                view: "AuthenticationController"
                self._connect_signal(view.controller.on_sign_in, "dashboard")
                self._connect_signal(
                    view.controller.on_sign_up, "role_selection"
                )
            case "dashboard":
                view: "DashboardController"
                self._connect_signal(
                    view.controller.on_sign_out, "authentication"
                )
            case "role_selection":
                view: "RoleSelectionController"
                self._connect_signal(
                    view.controller.on_customer_submit, "dashboard"
                )
                self._connect_signal(
                    view.controller.on_service_provider_submit,
                    "authentication"
                )
            case _:
                raise NotImplementedError(
                    f"Signals not implemented for view: {which_view!r}"
                )

    def clear_view_instance(self, which_view: str) -> None:
        if (view_params := self.view_map.get(which_view)) is None:
            raise ValueError(
                f"Unknown view requested for deletion: {which_view!r}"
            )
        if (view_inst := view_params['instance']) is None:
            raise ValueError(
                f"View pending deletion has no attributed " +
                f"instance: {which_view}"
            )
        self.stacked_widget.removeWidget(view_inst)
        view_inst.deleteLater()
        view_params['instance'] = None

