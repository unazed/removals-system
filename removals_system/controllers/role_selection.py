from PySide6.QtWidgets import QWidget


class RoleSelectionController:
    def __init__(self, view: QWidget, user_details: dict) -> None:
        self.view = view
        self.user_details = user_details

    def setup_connections(self) -> None:
        self.view.customer_card.clicked.connect(self.customer_card_selected)
        self.view.service_provider_card.clicked.connect(
            self.service_provider_card_selected
        )
    
    def customer_card_selected(self) -> None:
        print("Pressed customer")
    
    def service_provider_card_selected(self) -> None:
        print("Pressed service provider")