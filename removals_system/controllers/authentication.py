from PySide6.QtWidgets import QWidget, QMessageBox

from ..exceptions.auth_exceptions import InvalidCredentialsError
from ..models.user import User

from typing import final


@final
class AuthenticationController:
    def __init__(self, view: QWidget) -> None:
        self.view = view

    def setup_connections(self):
        self.view.login_form.sign_in_button.clicked.connect(self.handle_signin)
        self.view.signup_form.sign_up_button.clicked.connect(self.handle_signup)
        self.register_view_change_connections(
            self.view.signup_form.sign_in_prompt,
            self.view.login_form.sign_up_prompt,
            self.view.forgot_form.forgot_password_prompt,
            self.view.login_form.forgot_password_prompt
        )

    def register_view_change_connections(self, *widgets: QWidget):
        for widget in widgets:
            widget.linkActivated.connect(self.handle_view_link_clicked)

    def handle_view_link_clicked(self, link: str) -> None:
        match link:
            case 'sign-in':
                self.show_login_panel()
            case 'sign-up':
                self.show_signup_panel()
            case 'forgot-password':
                self.show_forgot_password_panel()
            case _:
                raise ValueError(f"Invalid authentication link: {link!r}")

    def handle_signin(self):
        login_data = self.view.login_form.get_data()
        try:
            user = User(**login_data)
        except InvalidCredentialsError:
            QMessageBox.information(self.view, "Failed", "Invalid credentials")
            return
        QMessageBox.information(self.view, "Success", user.jwt_token)
        

    def handle_signup(self):
        QMessageBox.information(self.view, "Success", "Account created!")
        self.show_login_panel()

    def show_login_panel(self) -> None:
        self.view.stack.setCurrentIndex(0)

    def show_signup_panel(self) -> None:
        self.view.stack.setCurrentIndex(1)

    def show_forgot_password_panel(self) -> None:
        self.view.stack.setCurrentIndex(2)