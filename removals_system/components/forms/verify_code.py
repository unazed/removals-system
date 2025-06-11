from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout,
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

from ...config.constants import ASSET_MAP

from ..line_edit import LineEdit
from ..primary_button import PrimaryButton
from ..primary_label import PrimaryLabel
from ..form import Form


class VerifyCodeForm(Form):
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

        title_label = QLabel("Forgot your password?")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Albert Sans", 16, QFont.Bold))

        caption_label = QLabel(
            "Receive a code to your email address to reset it"
        )
        caption_label.setAlignment(Qt.AlignCenter)
        caption_label.setFont(QFont("Albert Sans", 12))

        layout.addWidget(logo_label)
        layout.addSpacing(40)
        layout.addWidget(title_label)
        layout.addSpacing(4)
        layout.addWidget(caption_label)
        layout.addSpacing(40)

        self.code_input = LineEdit("Authentication code", name="code")
        self.password_input = LineEdit("Password", name="password")
        self.confirm_password_input = LineEdit(
            "Confirm password", name="confirm"
        )
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        layout.addWidget(self.code_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_password_input)
        layout.addSpacing(40)

        self.primary_button = PrimaryButton("Reset password")
        layout.addWidget(self.primary_button)

        layout.addStretch()

        self.signin_signup_prompt = PrimaryLabel("""
            <span style="font-weight: bold;">Done?</span>
            Click to
            <a href="sign-in"><span style="color:#89a69f;">sign in</span></a>
            or
            <a href="sign-up"><span style="color:#89a69f;">register</span></a>
        """)
        layout.addWidget(self.signin_signup_prompt)

        self.fields = (
            self.code_input,
            self.password_input,
            self.confirm_password_input
        )