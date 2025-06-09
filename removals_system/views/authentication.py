from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QSizePolicy,
    QHBoxLayout, QVBoxLayout, QStackedLayout
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

from ..components.line_edit import ModernLineEdit
from ..components.primary_button import PrimaryButton
from ..components.primary_label import PrimaryLabel
from ..components.forms.signup import SignupForm
from ..components.forms.login import LoginForm
from ..components.forms.forgot_password import ForgotPasswordForm
from ..components.forms.verify_code import VerifyCodeForm

from ..controllers.authentication import AuthenticationController

from ..config.constants import ASSET_MAP

from typing import final


@final
class AuthenticationView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Removals Service")
        self.controller = AuthenticationController(self)

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.create_branding_panel(), stretch=1)

        self.stack = QStackedLayout()
        self.login_form = LoginForm()
        self.signup_form = SignupForm()
        self.forgot_form = ForgotPasswordForm()
        self.verify_form = VerifyCodeForm()

        self.controller.setup_connections()

        self.stack.addWidget(self.login_form)
        self.stack.addWidget(self.signup_form)
        self.stack.addWidget(self.forgot_form)
        self.stack.addWidget(self.verify_form)

        container = QWidget()
        container.setLayout(self.stack)
        main_layout.addWidget(container, stretch=1)

        self.controller.show_login_panel()

    def create_branding_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        panel.setStyleSheet("background-color: #89a69f;")
        panel.setFont(QFont("Albert Sans", 10))
        layout.setContentsMargins(20, 20, 20, 20)

        image_label = QLabel()
        pixmap = QPixmap(ASSET_MAP['hero-truck'])
        image_label.setPixmap(
            pixmap.scaled(
                450, 300,
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)
        layout.addSpacing(5)

        tagline = QLabel("Smooth moves, fair prices")
        tagline.setStyleSheet(
            "color: white; font-weight: bold; font-size: 20px;"
        )
        tagline.setAlignment(Qt.AlignCenter)
        layout.addWidget(tagline)

        subtitle = QLabel(
            "Professional service, honest rates.\n" +
            "Start your journey with us today"
        )
        subtitle.setStyleSheet("color: white; font-size: 15px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(20)
        layout.addStretch()

        footer = QLabel("Serving Cardiff, Swansea & Newport")
        footer.setStyleSheet("color: white; font-size: 13px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        return panel