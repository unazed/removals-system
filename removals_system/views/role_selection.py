from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QStackedLayout, QVBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt

from ..components.forms.role_selection import RoleSelectionForm
from ..components.clickable_card import ClickableCard
from ..components.primary_button import PrimaryButton
from ..components.primary_label import PrimaryLabel
from ..components.line_edit import LineEdit
from ..components.combo_box import ComboBox
from ..components.date_picker import DatePicker
from ..components.form import Form

from ..controllers.role_selection import RoleSelectionController

from ..config.constants import ASSET_MAP


class RoleSelectionView(QWidget):
    def __init__(self, user_details: dict):
        super().__init__()

        self.setWindowTitle("Removals Service")
        self.controller = RoleSelectionController(self, user_details)

        self.cards: dict[str, ClickableCard] = {}
        
        main_layout = QHBoxLayout(self)
        self.stack = QStackedLayout()

        self.role_selection_form = self.create_role_selection_form(
            user_details['forename']
        )

        self.stack.addWidget(self.role_selection_form)
        self.controller.setup_connections()

        container = QWidget()
        container.setLayout(self.stack)
        main_layout.addWidget(container, stretch=1)

    def create_role_selection_form(self, forename: str) -> RoleSelectionForm:
        body_widget = Form()
        body_layout = QHBoxLayout(body_widget)
        body_layout.setSpacing(30)

        self.cards['customer'] = ClickableCard(
            "Customer",
            "I need help moving items to a new location, possibly including " +
            "packing, dismantling, or storage.",
            ASSET_MAP['customer-card'],
            (197, 170),
            parent=body_widget
        )

        self.cards['service-provider'] = ClickableCard(
            "Service Provider",
            "I want to offer professional moving services and connect with " +
            "people who need help relocating.",
            ASSET_MAP['service-provider-card'],
            (170, 170),
            parent=body_widget
        )

        for card_widget in self.cards.values():
            body_layout.addWidget(card_widget)

        return RoleSelectionForm(
            f"""
            Hi {forename},<br>
            tell us how you'd like to
            <span style="color:#89a69f;">use our service</span>
            """,
            body_widget,
            None
        )
    
    def create_customer_details_form(self) -> RoleSelectionForm:
        body_widget = Form()
        body_layout = QVBoxLayout(body_widget)
        
        country_widget = QWidget()
        country_layout = QHBoxLayout(country_widget)
        country_layout.setSpacing(15)
        country_field = ComboBox("Country", name="country")
        country_layout.addWidget(country_field)
        body_widget.fields.append(country_field)
        body_layout.addWidget(country_widget)

        county_city_widget = QWidget()
        county_city_layout = QHBoxLayout(county_city_widget)
        county_city_layout.setSpacing(15)
        city_field = ComboBox("City", name="city")
        county_field = ComboBox("County", name="county")
        county_city_layout.addWidget(county_field)
        county_city_layout.addWidget(city_field)
        body_widget.fields.extend((city_field, county_field))
        body_layout.addWidget(county_city_widget)

        telephone_dob_widget = QWidget()
        telephone_dob_layout = QHBoxLayout(telephone_dob_widget)
        telephone_dob_layout.setSpacing(15)
        telephone_field = LineEdit("Telephone", name="telephone")
        dob_field = DatePicker("Date of birth", name="dob")
        telephone_dob_layout.addWidget(telephone_field, stretch=1)
        telephone_dob_layout.addWidget(dob_field, stretch=1)
        body_widget.fields.extend((telephone_field, dob_field))
        body_layout.addWidget(telephone_dob_widget)

        address_widget = QWidget()
        address_layout = QHBoxLayout(address_widget)
        address_layout.setSpacing(15)
        address_line_1 = LineEdit("Address Line 1", name="address-1")
        address_line_2 = LineEdit("Line 2", name="address-2")
        address_line_2.set_optional(True)
        post_code = LineEdit("Post code", name="post-code")
        address_layout.addWidget(post_code)
        address_layout.addWidget(address_line_1)
        address_layout.addWidget(address_line_2)
        body_widget.fields.extend(
            (address_line_1, address_line_2, post_code)
        )
        body_layout.addWidget(address_widget)

        footer_widget = QWidget()
        footer_layout = QVBoxLayout(footer_widget)
        footer_layout.setSpacing(10)

        body_widget.primary_button = PrimaryButton("Finish")
        body_widget.primary_button.setFixedWidth(250)
        back_label = PrimaryLabel("""
            or go <a href="back"><span style="color:#89a69f">back</span></a>
        """)
        footer_layout.addWidget(
            body_widget.primary_button, alignment=Qt.AlignCenter
        )
        footer_layout.addWidget(back_label)

        return RoleSelectionForm(
            f"""
            Thank you for choosing us. We just need a little bit more
            <span style="color:#89a69f;">information</span>
            about you.
            """,
            body_widget,
            footer_widget
        )