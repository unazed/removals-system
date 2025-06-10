import typing
if typing.TYPE_CHECKING:
    from ..views.role_selection import RoleSelectionView
    from ..components.form_widget import FormWidget


class RoleSelectionController:
    def __init__(self, view: "RoleSelectionView", user_details: dict) -> None:
        self.view = view
        self.user_details = user_details

        self.card_callback_map = {
            "customer": self.customer_card_selected,
            "service-provider": self.service_provider_card_selected
        }
        self.current_view: str | None = None

    def setup_connections(self) -> None:
        for which, callback in self.card_callback_map.items():
            self.view.cards[which].clicked.connect(callback)
    
    def customer_card_selected(self) -> None:
        self.current_view = "customer"
        details_form = self.view.create_customer_details_form()
        details_form.body.on_submit(self.customer_submit_details)
        self.view.stack.addWidget(details_form)
        self.view.stack.setCurrentIndex(1)
    
    def customer_submit_details(self, form: "FormWidget") -> None:
        print(form.get_data())
    
    def service_provider_card_selected(self) -> None:
        print("Pressed service provider")
