from typing import final
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QSizePolicy, QHBoxLayout, QVBoxLayout,
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

from ..components.form import Form
from ..config.constants import ASSET_MAP

from .line_edit import ModernLineEdit
from .primary_button import PrimaryButton
from .primary_label import PrimaryLabel


@final
class SignupForm(QWidget, Form):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(12)

        logo_label = QLabel()
        logo_pixmap = QPixmap(ASSET_MAP['logo-black'])
        logo_label.setPixmap(
            logo_pixmap.scaled(
                152, 65,
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        logo_label.setAlignment(Qt.AlignCenter)

        layout.addSpacing(40)
        layout.addWidget(logo_label)

        title_label = QLabel("Sign up")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Albert Sans", 16, QFont.Bold))

        layout.addWidget(logo_label)
        layout.addSpacing(40)
        layout.addWidget(title_label)
        layout.addSpacing(40)

        self.email_input = ModernLineEdit("Email", name="email")
        layout.addWidget(self.email_input)

        name_inputs = QWidget()
        name_layout = QHBoxLayout(name_inputs)
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setSpacing(12)

        self.forename_input = ModernLineEdit("Forename", name="forename")
        self.surname_input = ModernLineEdit("Surname", name="surname")

        self.forename_input.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred
        )
        self.surname_input.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred
        )

        name_layout.addWidget(self.forename_input)
        name_layout.addWidget(self.surname_input)
        layout.addWidget(name_inputs)

        self.password_input = ModernLineEdit("Password", name="password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.confirm_password_input = ModernLineEdit(
            "Confirm password", name="confirm"
        )
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password_input)
        layout.addSpacing(40)

        self.sign_up_button = PrimaryButton("Sign up")
        layout.addWidget(self.sign_up_button)
        layout.addSpacing(40)
        layout.addStretch()

        self.sign_in_prompt = PrimaryLabel("""
            <span style="font-weight: bold;">Already have an account?</span>
            When you're ready,
            <a href="sign-in"><span style="color:#89a69f;">sign in</span></a>
        """)
        layout.addWidget(self.sign_in_prompt)

        self.fields = (
            self.email_input,
            self.forename_input,
            self.surname_input,
            self.password_input,
            self.confirm_password_input
        )