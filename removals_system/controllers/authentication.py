from PySide6.QtWidgets import QWidget

from ..exceptions.auth_exceptions import InvalidCredentialsError
from ..models.user import User, exists_email, is_valid_email

from ..views.role_selection import RoleSelectionView

from typing import final


@final
class AuthenticationController:
    def __init__(self, view: QWidget) -> None:
        self.view = view

    def setup_connections(self):
        self.view.login_form.on_submit(self.handle_signin)
        self.view.signup_form.on_submit(self.handle_signup)
        self.view.forgot_form.on_submit(self.handle_forgot_password)
        self.view.verify_form.on_submit(self.handle_code_verify)

        self.register_view_change_connections(
            self.view.signup_form.sign_in_prompt,
            self.view.login_form.sign_up_prompt,
            self.view.forgot_form.signin_signup_prompt,
            self.view.login_form.forgot_password_prompt,
            self.view.verify_form.signin_signup_prompt
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
                raise RuntimeError(f"Invalid authentication link: {link!r}")

    def handle_signin(self):
        login_data = self.view.login_form.get_data()
        
        if self.view.login_form.is_empty_fields():
            return

        try:
            user = User(**login_data)
        except InvalidCredentialsError:
            self.view.login_form.email_input.set_state("error")
            self.view.login_form.password_input.set_state("error")
            return
        
        # TODO: go-to customer/SP dashboard

    def handle_signup(self):
        signup_data = self.view.signup_form.get_data()

        if self.view.signup_form.is_empty_fields():
            return

        if signup_data['password'] != signup_data['confirm']:
            self.view.signup_form.password_input.set_state("error")
            self.view.signup_form.confirm_password_input.set_state("error")
            return
        
        if not is_valid_email(signup_data['email']):
            self.view.signup_form.email_input.set_state("error")
            return

        if exists_email(signup_data['email']):
            self.view.signup_form.email_input.set_state("error")
            return
    
        role_selection_view = RoleSelectionView(signup_data)
        role_selection_view.show()
        self.view.close()

    def handle_forgot_password(self) -> None:
        email = self.view.forgot_form.get_data()['email']

        if self.view.forgot_form.is_empty_fields():
            return

        if not exists_email(email):
            self.view.forgot_form.email_input.set_state("error")
            return
        
        self.show_verify_code_panel()

    def handle_code_verify(self) -> None:
        verify_data = self.view.verify_form.get_data()

        if self.view.verify_form.is_empty_fields():
            return

        if verify_data['password'] != verify_data['confirm']:
            self.view.verify_form.password_input.set_state("error")
            self.view.verify_form.confirm_password_input.set_state("error")
            return

        print("Pretending to verify code:", verify_data['code'])
        self.show_login_panel()

    def show_login_panel(self) -> None:
        self.view.stack.setCurrentIndex(0)

    def show_signup_panel(self) -> None:
        self.view.stack.setCurrentIndex(1)

    def show_forgot_password_panel(self) -> None:
        self.view.stack.setCurrentIndex(2)
    
    def show_verify_code_panel(self) -> None:
        self.view.stack.setCurrentIndex(3)