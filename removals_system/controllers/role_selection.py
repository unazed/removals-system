from PySide6.QtCore import Qt, Signal, QObject

from ..models.user import User, register_user
from ..models.addresses import get_countries, get_counties, get_cities
from ..models.telephone import is_valid_number, extract_phone_components
from ..models.db import proc_get_length_constraint
from ..models.db_types import get_type_values
from ..components.forms.util_validation import validate_age_over_18
from ..components import PrimaryLabel

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from ..views import RoleSelectionView
    from ..components.forms import RoleSelectionForm
    from ..components import (
        ComboBox, DatePicker, LineEdit, Form, ItemInput
    )


class RoleSelectionController(QObject):
    on_customer_submit = Signal(User)
    on_service_provider_submit = Signal()

    def __init__(self, view: "RoleSelectionView", user_auth: dict) -> None:
        super().__init__()
        self.view = view
        self.user_auth = user_auth

        self.card_callback_map = {
            "customer": self.customer_card_selected,
            "service-provider": self.service_provider_card_selected
        }

    def setup_card_connections(self) -> None:
        for which, callback in self.card_callback_map.items():
            self.view.cards[which].clicked.connect(callback)
    
    def customer_card_selected(self) -> None:
        details_form = self.view.create_customer_form()
        self.register_details_connections(details_form)
        self.register_link_labels(details_form)
        details_form.body.on_submit(self.customer_submit_details)
        self.view.stack.addWidget(details_form)
        self.view.stack.setCurrentIndex(1)

    def service_provider_card_selected(self) -> None:
        details, business_info, final\
            = self.view.create_service_provider_forms()

        self.register_details_connections(details)
        self.register_business_connections(business_info)
        self.register_link_labels(details, business_info, final)

        details.body.on_submit(self.service_provider_submit_details)
        business_info.body.on_submit(
            self.service_provider_submit_business_details
        )

        self.view.stack.addWidget(details)
        self.view.stack.addWidget(business_info)
        self.view.stack.addWidget(final)

        self.view.stack.setCurrentIndex(1)

    def service_provider_submit_details(
        self,
        form: "Form"
    ) -> None:
        if not form.is_valid_fields():
            return
        self.view.stack.setCurrentIndex(2)
    
    def service_provider_submit_business_details(
        self,
        form: "Form"
    ) -> None:
        if not form.is_valid_fields():
            return
        service_provider_details: "Form" = self.view.stack.widget(1).body
        user = self.register_user_from_detail_form(
            service_provider_details,
            "service-provider"
        )
        self.view.stack.setCurrentIndex(3)

    def register_user_from_detail_form(
        self,
        detail_form: "Form",
        role: str
    ) -> User:
        user_details = form.get_data()
        user = register_user(**{
            "forename": self.user_auth['forename'],
            "surname": self.user_auth['surname'],
            "email": self.user_auth['email'],
            "password": self.user_auth['password'],
            "dob": user_details['dob'].toPython(),
            "role": "customer"
        })
        user.create_address(
            user_details['city'], user_details['county'],
            user_details['country'], user_details['post-code'],
            user_details['address-1'], user_details['address-2']
        )
        number_info = extract_phone_components(
            user_details['home-telephone']
        )
        user.create_phone_number(*number_info)
        if (work_number := user_details.get('work-telephone')) is not None:
            number_info = extract_phone_components(work_number)
            user.create_phone_number(*number_info, phone_type="work")
        return user

    def customer_submit_details(self, form: "Form") -> None:
        if not form.is_valid_fields():
            return
        self.on_customer_submit.emit(
            self.register_user_from_detail_form(form),
            "customer"
        )

    def register_link_labels(self, *forms: "RoleSelectionForm") -> None:
        for form in forms:
            label = form.findChild(PrimaryLabel)
            if label is not None:
                label.linkActivated.connect(self.handle_back_label)

    def register_validation_if_exists(
        form: "RoleSelectionForm",
        widget_name: str,
        function: callable
    ) -> None:
        widget = form.body.get_widget(widget_name)
        if widget is not None:
            widget.register_validation_func(function)

    def register_business_connections(self, form: "RoleSelectionForm") -> None:
        item_input: "ItemInput" = form.body.get_widget("items")
        item_input.add_combo_items(*get_type_values("BusinessResourceTypes"))

        self.register_validation_if_exists(
            form, "nr-employees",
            lambda n: n.isdecimal() and int(n) > 0
        )
        self.register_validation_if_exists(
            form, "crn",
            lambda crn: len(crn) == 8
        )
        self.register_validation_if_exists(
            form, "vat-number",
            lambda vat: len(vat) == 11
        )
        self.register_validation_if_exists(
            form, "utr-number",
            lambda utr: len(utr) == 10
        )

    def register_details_connections(self, form: "RoleSelectionForm") -> None:
        country_combo: "ComboBox" = form.body.get_widget("country")
        if country_combo is not None:
            for country_code, country_name in get_countries():
                country_combo.addItem(country_name)
                country_combo.setItemData(
                    country_combo.count() - 1,
                    country_code,
                    Qt.UserRole
                )
            country_combo.currentTextChanged.connect(
                lambda to: self.on_country_change(form, to)
            )
            county_combo: "ComboBox" = form.body.get_widget("county")
            county_combo.currentTextChanged.connect(
                lambda to: self.on_county_change(form, to)
            )

        self.register_validation_if_exists(
            form, "dob",
            validate_age_over_18
        )
        self.register_validation_if_exists(
            form, "home-telephone",
            is_valid_number
        )
        self.register_validation_if_exists(
            form, "work-telephone",
            is_valid_number
        )

        post_code: "LineEdit" = form.body.get_widget("post-code")
        if post_code is not None:
            post_code.setMaxLength(
                proc_get_length_constraint("addresses", "post_code")
            )

    def handle_back_label(self, where: str) -> None:
        match where:
            case "back":
                self.view.stack.setCurrentIndex(
                    max(0, self.view.stack.currentIndex() - 1)
                )
            case "sign-in":
                self.on_service_provider_submit.emit()
            case _:
                raise RuntimeError(f"Invalid back-label with href: {where}")

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
