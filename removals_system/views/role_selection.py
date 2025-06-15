from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QStackedLayout, QVBoxLayout, QSizePolicy, QLabel
)
from PySide6.QtGui import QPixmap
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

        self.setWindowTitle("Role selection")
        self.controller = RoleSelectionController(self, user_details)

        self.cards: dict[str, ClickableCard] = {}
        
        main_layout = QHBoxLayout(self)
        self.stack = QStackedLayout()

        self.role_selection_form = self.create_role_selection_form(
            user_details['forename']
        )

        self.stack.addWidget(self.role_selection_form)
        self.controller.setup_card_connections()

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
    
    def create_service_provider_forms(self) -> tuple[RoleSelectionForm]:
        return (
            self.create_service_provider_detail_form(),
            self.create_service_provider_business_form(),
            self.create_service_provider_pending_form()
        )

    def create_service_provider_detail_form(self) -> RoleSelectionForm:
        body_widget = Form()
        body_layout = QVBoxLayout(body_widget)

        def add_field_row(*fields: QWidget, stretch: bool = True):
            row = QWidget()
            layout = QHBoxLayout(row)
            layout.setSpacing(15)
            for field in fields:
                layout.addWidget(field, stretch=1 if stretch else 0)
                body_widget.fields.append(field)
            body_layout.addWidget(row)

        add_field_row(
            LineEdit("Address Line 1", name="address-1"),
            LineEdit("Line 2", name="address-2")\
                .set_optional(True),
            LineEdit("Post code", name="post-code")
        )

        add_field_row(
            ComboBox("Country", name="country"),
            LineEdit("Home telephone", name="home-telephone")
        )

        add_field_row(
            ComboBox("County", name="county"),
            LineEdit("Work telephone", name="work-telephone")\
                .set_optional(True)
        )

        add_field_row(
            ComboBox("City", name="city"),
            DatePicker("Date of birth", name="dob")
        )

        footer_widget = QWidget()
        footer_layout = QVBoxLayout(footer_widget)
        footer_layout.setSpacing(10)

        body_widget.primary_button = PrimaryButton("Continue")
        body_widget.primary_button.setFixedWidth(250)

        back_label = PrimaryLabel("""
            or go <a href="back"><span style="color:#89a69f">back</span></a>
        """)

        footer_layout.addWidget(
            body_widget.primary_button, alignment=Qt.AlignCenter
        )
        footer_layout.addWidget(back_label)

        return RoleSelectionForm(
            """
            Thank you for working with us. We just need a little bit more
            <span style="color:#89a69f;">information</span>
            about you.
            """,
            body_widget,
            footer_widget
        )

    def create_service_provider_business_form(self) -> RoleSelectionForm:
        body_widget = Form()
        body_layout = QVBoxLayout(body_widget)

        footer_widget = QWidget()
        footer_layout = QVBoxLayout(footer_widget)
        footer_layout.setSpacing(10)

        body_widget.primary_button = PrimaryButton("Continue")
        body_widget.primary_button.setFixedWidth(250)
        back_label = PrimaryLabel("""
            or go <a href="back"><span style="color:#89a69f">back</span></a>
        """)
        footer_layout.addWidget(
            body_widget.primary_button, alignment=Qt.AlignCenter
        )
        footer_layout.addWidget(back_label)

        return RoleSelectionForm(
            """
            Tell us what you're
            <span style="color:#89a69f;">working</span>
            with
            """,
            body_widget,
            footer_widget
        )

    def create_service_provider_pending_form(self) -> RoleSelectionForm:
        body_widget = Form()
        body_layout = QVBoxLayout(body_widget)

        logo_pixmap = QPixmap(ASSET_MAP['fireworks'])
        logo_label = QLabel()
        logo_label.setPixmap(
            logo_pixmap.scaled(
                210, 210,
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        logo_label.setAlignment(Qt.AlignCenter)
        body_layout.addWidget(logo_label)
        body_layout.addSpacing(20)

        subtitle_label = QLabel("All done on your end!")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        body_layout.addWidget(subtitle_label)
        body_layout.addSpacing(10)

        caption_label = QLabel(
            "We’re reviewing your information and will drop you an email " +
            "as soon as everything’s good to go."
        )
        caption_label.setWordWrap(True)
        caption_label.setAlignment(Qt.AlignCenter)
        caption_label.setStyleSheet("font-size: 16px; color: #666;")
        body_layout.addWidget(caption_label)

        footer_widget = QWidget()
        footer_layout = QVBoxLayout(footer_widget)
        footer_layout.setSpacing(10)

        back_label = PrimaryLabel("""
            back to
            <a href="sign-in"><span style="color:#89a69f">sign in</span></a>
        """)
        footer_layout.addWidget(back_label)

        return RoleSelectionForm(
            """
            We'll be in <span style="color:#89a69f;">touch soon</span>
            """,
            body_widget,
            footer_widget
        )

    def create_customer_form(self) -> RoleSelectionForm:
        body_widget = Form()
        body_layout = QVBoxLayout(body_widget)

        def add_field_row(*fields: QWidget, stretch: bool = True):
            row = QWidget()
            layout = QHBoxLayout(row)
            layout.setSpacing(15)
            for field in fields:
                layout.addWidget(field, stretch=1 if stretch else 0)
                body_widget.fields.append(field)
            body_layout.addWidget(row)

        add_field_row(
            ComboBox("Country", name="country"),
            stretch=False
        )

        add_field_row(
            ComboBox("County", name="county"),
            ComboBox("City", name="city")
        )

        add_field_row(
            LineEdit("Telephone", name="home-telephone"),
            DatePicker("Date of birth", name="dob")
        )

        add_field_row(
            LineEdit("Post code", name="post-code"),
            LineEdit("Address Line 1", name="address-1"),
            LineEdit("Line 2", name="address-2")\
                .set_optional(True)
        )

        footer_widget = QWidget()
        footer_layout = QVBoxLayout(footer_widget)
        footer_layout.setSpacing(10)

        body_widget.primary_button = PrimaryButton("Continue")
        body_widget.primary_button.setFixedWidth(250)

        back_label = PrimaryLabel("""
            or go <a href="back"><span style="color:#89a69f">back</span></a>
        """)

        footer_layout.addWidget(
            body_widget.primary_button, alignment=Qt.AlignCenter
        )
        footer_layout.addWidget(back_label)

        return RoleSelectionForm(
            """
            Thank you for choosing us. We just need a little bit more
            <span style="color:#89a69f;">information</span>
            about you.
            """,
            body_widget,
            footer_widget
        )