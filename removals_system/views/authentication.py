from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QSizePolicy,
    QHBoxLayout, QVBoxLayout, QStackedLayout
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

from ..components.line_edit import ModernLineEdit
from ..components.primary_button import PrimaryButton
from ..components.primary_label import PrimaryLabel
from ..controllers.authentication import AuthenticationController
from ..constants import ASSET_MAP

from typing import final


@final
class AuthenticationView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Removals Service")
        self.controller = AuthenticationController(self)

        self.sign_in_button: QPushButton | None = None
        self.sign_up_button: QPushButton | None = None
        self.sign_in_prompt: QLabel | None = None
        self.sign_up_prompt: QLabel | None = None

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.create_branding_panel(), stretch=1)

        self.stack = QStackedLayout()
        self.login_panel = self.create_login_panel()
        self.panel = self.create_panel()
        self.forgot_panel = self.create_forgot_password_panel()

        self.controller.setup_connections()

        _ = self.stack.addWidget(self.login_panel)
        _ = self.stack.addWidget(self.panel)
        _ = self.stack.addWidget(self.forgot_panel)

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

    def create_login_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
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

        email_input = ModernLineEdit("Email")
        layout.addWidget(email_input)

        password_input = ModernLineEdit("Password")
        password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_input)

        forgot_password = QLabel("""
            <a href="forgot-password"><span style="color:#89a69f;"> 
                Forgot password?
            </span></a>
        """)
        forgot_password.setTextFormat(Qt.RichText)
        forgot_password.setTextInteractionFlags(Qt.TextBrowserInteraction)
        forgot_password.setOpenExternalLinks(False)
        forgot_password.setAlignment(Qt.AlignRight)
        forgot_password.setStyleSheet("""
            QLabel {
                color: #89a69f;
                font-size: 10px;
            }
            a {
                text-decoration: none;
            }
        """)
        _ = forgot_password.linkActivated.connect(
            self.controller.show_forgot_password_panel
        )

        layout.addWidget(forgot_password)
        layout.addSpacing(40)

        self.sign_in_button = PrimaryButton("Sign in")
        layout.addWidget(self.sign_in_button)

        layout.addStretch()

        self.sign_up_prompt = PrimaryLabel("""
            <span style="font-weight: bold;">New to us?</span>
            Create your
            <a href="sign-up"><span style="color:#89a69f;">account</span></a>,
            and let us make your life easier.
        """)
        layout.addWidget(self.sign_up_prompt)

        return panel

    def create_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
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

        email_input = ModernLineEdit("Email")
        layout.addWidget(email_input)

        name_inputs = QWidget()
        name_layout = QHBoxLayout(name_inputs)
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setSpacing(12)

        forename_input = ModernLineEdit("Forename")
        surname_input = ModernLineEdit("Surname")

        forename_input.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred
        )
        surname_input.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred
        )

        name_layout.addWidget(forename_input)
        name_layout.addWidget(surname_input)
        layout.addWidget(name_inputs)

        password_input = ModernLineEdit("Password")
        password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_input)

        confirm_password_input = ModernLineEdit(
            "Confirm password"
        )
        confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(confirm_password_input)
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

        return panel

    def create_forgot_password_panel(self) -> QWidget:
        panel = QWidget()

        layout = QVBoxLayout(panel)
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

        layout.addWidget(logo_label)
        layout.addSpacing(40)
        layout.addWidget(title_label)
        layout.addSpacing(40)

        layout.addStretch()

        self.forgot_password_prompt = PrimaryLabel("""
            <span style="font-weight: bold;">Done?</span>
            <a href="sign-in"><span style="color:#89a69f;">Sign in</span></a>
            or
            <a href="sign-up"><span style="color:#89a69f;">register</span></a>
        """)
        layout.addWidget(self.forgot_password_prompt)

        return panel