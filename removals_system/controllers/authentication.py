from PySide6.QtWidgets import QWidget, QMessageBox

from typing import final


@final
class AuthenticationController:
    def __init__(self, view: QWidget) -> None:
        self.view = view

    def setup_connections(self):
        self.view.sign_in_button.clicked.connect(self.handle_signin)
        self.view.sign_up_button.clicked.connect(self.handle_signup)
        self.view.sign_in_prompt.linkActivated.connect(self.handle_link_clicked)
        self.view.sign_up_prompt.linkActivated.connect(self.handle_link_clicked)
        self.view.forgot_password_prompt.linkActivated.connect(
            self.handle_link_clicked
        )

    def handle_link_clicked(self, link: str) -> None:
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
        QMessageBox.information(self.view, "Success", "Signed in!")
        self.show_login_panel()

    def handle_signup(self):
        QMessageBox.information(self.view, "Success", "Account created!")
        self.show_login_panel()

    def show_login_panel(self) -> None:
        self.view.stack.setCurrentIndex(0)

    def show_signup_panel(self) -> None:
        self.view.stack.setCurrentIndex(1)

    def show_forgot_password_panel(self) -> None:
        self.view.stack.setCurrentIndex(2)