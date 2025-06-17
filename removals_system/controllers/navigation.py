from PySide6.QtWidgets import QMainWindow, QStackedWidget
from typing import TYPE_CHECKING, Dict, Any, Optional, Callable
from functools import partial
import importlib

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget
    from PySide6.QtCore import Signal
    from . import (
        AuthenticationController,
        DashboardController,
        RoleSelectionController
    )


class NavigationController(QMainWindow):
    def __init__(self, default_view: str) -> None:
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.view_map = {
            "authentication": {
                "module_path": "..views",
                "class_name": "AuthenticationView",
                "class": None,
                "instance": None,
                "reusable": False
            },
            "role_selection": {
                "module_path": "..views",
                "class_name": "RoleSelectionView", 
                "class": None,
                "instance": None,
                "reusable": False
            },
            "dashboard": {
                "module_path": "..views",
                "class_name": "DashboardView",
                "class": None,
                "instance": None,
                "reusable": False
            }
        }

        self.show_view(default_view)

    def _load_view_class(self, which_view: str) -> type:
        view_params = self.view_map[which_view]
        
        if view_params['class'] is None:
            base_package = __name__.split('.')[0]
            module_path = f"{base_package}.views"
            module = importlib.import_module(module_path)
            view_class = getattr(module, view_params['class_name'])
            view_params['class'] = view_class
            
        return view_params['class']

    def show_view(self, which_view: str, *args, **kwargs) -> None:
        if which_view not in self.view_map:
            raise ValueError(f"Unknown view requested: {which_view!r}")

        view_params = self.view_map[which_view]
        
        if (view_inst := view_params['instance']) is not None:
            if view_params['reusable']:
                self.stacked_widget.setCurrentWidget(view_inst)
                return
            self.clear_view_instance(which_view)
        
        view_class = self._load_view_class(which_view)
        view_inst = view_class(*args, **kwargs)
        
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