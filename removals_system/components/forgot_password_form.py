from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

from ..config.constants import ASSET_MAP

from .primary_label import PrimaryLabel

from typing import final


@final
class ForgotPasswordForm(QWidget):
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