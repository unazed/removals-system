from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStackedLayout
)

from ..components.forms.role_selection import RoleSelectionForm
from ..components.clickable_card import ClickableCard
from ..controllers.role_selection import RoleSelectionController
from ..config.constants import ASSET_MAP


class RoleSelectionView(QWidget):
    def __init__(self, user_details: dict):
        super().__init__()

        self.setWindowTitle("Removals Service")
        self.controller = RoleSelectionController(self, user_details)

        main_layout = QHBoxLayout(self)

        self.stack = QStackedLayout()

        body_widget = QWidget()
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(30)

        self.customer_card = ClickableCard(
            "Customer",
            "I need help moving items to a new location, possibly including " +
            "packing, dismantling, or storage.",
            ASSET_MAP['customer-card'],
            (197, 170)
        )
        self.service_provider_card = ClickableCard(
            "Service Provider",
            "I want to offer professional moving services and connect with " +
            "people who need help relocating.",
            ASSET_MAP['service-provider-card'],
            (170, 170)
        )
        body_layout.addWidget(self.customer_card)
        body_layout.addWidget(self.service_provider_card)

        self.role_selection_form = RoleSelectionForm(
            f"""
            Hi {user_details['forename']},<br>
            tell us how you'd like to
            <span style="color:#89a69f;">use our service</span>
            """,
            body_widget,
            None
        )

        self.stack.addWidget(self.role_selection_form)

        self.controller.setup_connections()

        container = QWidget()
        container.setLayout(self.stack)
        main_layout.addWidget(container, stretch=1)
