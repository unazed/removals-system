from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout,
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

from ...config.constants import ASSET_MAP
from ...models.user import is_valid_email, exists_email

from ..line_edit import LineEdit
from ..primary_button import PrimaryButton
from ..primary_label import PrimaryLabel

from .form import Form

from typing import final


@final
class LoginForm(QWidget, Form):
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

        title_label = QLabel("Sign in")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Albert Sans", 16, QFont.Bold))

        layout.addWidget(logo_label)
        layout.addSpacing(40)
        layout.addWidget(title_label)
        layout.addSpacing(40)

        self.email_input = LineEdit("Email", name="email")
        self.email_input.register_validation_func(
            lambda email: is_valid_email(email) and exists_email(email)
        )
        layout.addWidget(self.email_input)

        self.password_input = LineEdit("Password", name="password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.forgot_password_prompt = PrimaryLabel("""
            <a href="forgot-password"><span style="color:#89a69f;"> 
                Forgot password?
            </span></a>
        """)
        self.forgot_password_prompt.setAlignment(Qt.AlignRight)

        layout.addWidget(self.forgot_password_prompt)
        layout.addSpacing(40)

        self.primary_button = PrimaryButton("Sign in")
        layout.addWidget(self.primary_button)

        layout.addStretch()

        self.sign_up_prompt = PrimaryLabel("""
            <span style="font-weight: bold;">New to us?</span>
            Create your
            <a href="sign-up"><span style="color:#89a69f;">account</span></a>,
            and let us make your life easier.
        """)
        layout.addWidget(self.sign_up_prompt)

        self.fields = [
            self.email_input,
            self.password_input
        ]