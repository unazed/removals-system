from PySide6.QtCore import Qt, Signal, QObject

from ..models.user import User, register_user
from ..models.addresses import get_countries, get_counties, get_cities
from ..models.telephone import is_valid_number, extract_phone_components
from ..models.db import proc_get_length_constraint
from ..views.dashboard import DashboardView
from ..components.forms.util_validation import validate_age_over_18
from ..components.primary_label import PrimaryLabel

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from ..views.role_selection import RoleSelectionView
    from ..components.forms.role_selection import RoleSelectionForm
    from ..components.combo_box import ComboBox
    from ..components.date_picker import DatePicker
    from ..components.line_edit import LineEdit
    from ..components.form import Form


class RoleSelectionController(QObject):
    on_customer_submit = Signal(User)
    on_service_provider_submit = Signal()

    def __init__(self, view: "RoleSelectionView", user_details: dict) -> None:
        super().__init__()
        self.view = view
        self.user_details = user_details

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
        form: "RoleSelectionForm"
    ) -> None:
        if not form.is_valid_fields():
            return
        self.view.stack.setCurrentIndex(2)
    
    def service_provider_submit_business_details(
        self,
        form: "RoleSelectionForm"
    ) -> None:
        if not form.is_valid_fields():
            return
        self.view.stack.setCurrentIndex(3)

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
        user.create_address(
            extra_user_info['city'], extra_user_info['county'],
            extra_user_info['country'], extra_user_info['post-code'],
            extra_user_info['address-1'], extra_user_info['address-2']
        )
        ext, number = extract_phone_components(
            extra_user_info['home-telephone']
        )
        user.create_phone_number(ext, number)
        self.on_customer_submit.emit(user)

    def register_link_labels(self, *forms: "RoleSelectionForm") -> None:
        for form in forms:
            label = form.findChild(PrimaryLabel)
            if label is not None:
                label.linkActivated.connect(self.handle_back_label)

    def register_business_connections(self, form: "RoleSelectionForm") -> None:
        pass
    
    def register_details_connections(self, form: "RoleSelectionForm") -> None:
        def register_validation_if_exists(
            widget_name: str,
            function: callable
        ) -> None:
            widget = form.body.get_widget(widget_name)
            if widget is not None:
                widget.register_validation_func(function)

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

        register_validation_if_exists("dob", validate_age_over_18)
        register_validation_if_exists("home-telephone", is_valid_number)
        register_validation_if_exists("work-telephone", is_valid_number)

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
