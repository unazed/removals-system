from PySide6.QtCore import Qt

from ..models.user import register_user
from ..models.addresses import get_countries, get_counties, get_cities
from ..models.telephone import is_valid_number
from ..models.db import proc_get_length_constraint
from ..views.dashboard import DashboardView
from ..components.forms.util_validation import validate_age_over_18

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from ..views.role_selection import RoleSelectionView
    from ..components.forms.role_selection import RoleSelectionForm
    from ..components.combo_box import ComboBox
    from ..components.date_picker import DatePicker
    from ..components.line_edit import LineEdit
    from ..components.form import Form


class RoleSelectionController:
    def __init__(self, view: "RoleSelectionView", user_details: dict) -> None:
        self.view = view
        self.user_details = user_details

        self.card_callback_map = {
            "customer": self.customer_card_selected,
            "service-provider": self.service_provider_card_selected
        }
        self.current_view: Literal['customer', 'service-provider'] | None \
            = None

    def setup_connections(self) -> None:
        for which, callback in self.card_callback_map.items():
            self.view.cards[which].clicked.connect(callback)
    
    def customer_card_selected(self) -> None:
        self.current_view = "customer"
        details_form = self.view.create_customer_details_form()
        self.register_customer_details_connections(details_form)
        details_form.body.on_submit(self.customer_submit_details)
        self.view.stack.addWidget(details_form)
        self.view.stack.setCurrentIndex(1)

    def register_customer_details_connections(
        self,
        details_form: "RoleSelectionForm"
    ) -> None:
        country_combo: "ComboBox" = details_form.body.get_widget("country")
        for country_code, country_name in get_countries():
            country_combo.addItem(country_name)
            country_combo.setItemData(
                country_combo.count() - 1,
                country_code,
                Qt.UserRole
            )
        country_combo.currentTextChanged.connect(
            lambda to: self.on_country_change(details_form, to)
        )
        county_combo: "ComboBox" = details_form.body.get_widget("county")
        county_combo.currentTextChanged.connect(
            lambda to: self.on_county_change(details_form, to)
        )
        dob_date: "DatePicker" = details_form.body.get_widget("dob")
        dob_date.register_validation_func(validate_age_over_18)
        telephone_field: "LineEdit" = details_form.body.get_widget("telephone")
        telephone_field.register_validation_func(is_valid_number)
        post_code: "LineEdit" = details_form.body.get_widget("post-code")
        post_code.setMaxLength(
            proc_get_length_constraint("addresses", "post_code")
        )

    def on_country_change(
        self,
        form: "RoleSelectionForm",
        country: str
    ) -> None:
        county_combo: ComboBox = form.body.get_widget("county")
        county_combo.clear()
        county_combo.addItems(get_counties(country))

    def on_county_change(
        self,
        form: "RoleSelectionForm",
        county: str
    ) -> None:
        country_combo: ComboBox = form.body.get_widget("country")
        cities_combo: ComboBox = form.body.get_widget("city")
        cities_combo.clear()
        cities_combo.addItems(get_cities(country_combo.serialize(), county))
    
    def customer_submit_details(self, form: "Form") -> None:
        if not form.is_valid_fields():
            return
        extra_user_info = form.get_data()
        user = register_user(**{
            "forename": self.user_details['forename'],
            "surname": self.user_details['surname'],
            "email": self.user_details['email'],
            "password": self.user_details['password'],
            "dob": extra_user_info['dob'].toPython(),
            "role": "customer"
        })
        self.dashboard = Dashboard(user)
        self.view.close()
        self.dashboard.show()
    
    def service_provider_card_selected(self) -> None:
        self.current_view = "service-provider"
        print("Pressed service provider")
