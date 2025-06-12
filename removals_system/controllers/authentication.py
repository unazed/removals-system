from ..exceptions.auth_exceptions import InvalidCredentialsError
from ..models.user import User, exists_email

from ..views.role_selection import RoleSelectionView
from ..views.dashboard import Dashboard

from typing import final, TYPE_CHECKING
if TYPE_CHECKING:
    from ..components.primary_label import PrimaryLabel
    from ..components.forms.login import LoginForm
    from ..components.forms.signup import SignupForm
    from ..components.forms.forgot_password import ForgotPasswordForm
    from ..components.forms.verify_code import VerifyCodeForm
    from ..views.authentication import AuthenticationView


@final
class AuthenticationController:
    def __init__(self, view: "AuthenticationView") -> None:
        self.view = view
        self._role_selection_view: RoleSelectionView | None = None

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

    def register_view_change_connections(self, *widgets: "PrimaryLabel"):
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

    def handle_signin(self, form: "LoginForm") -> None:
        login_data = form.get_data()
        
        if not form.is_valid_fields():
            return

        try:
            user = User(**login_data)
        except InvalidCredentialsError:
            form.set_all_invalid()
            return
        
        self.dashboard = Dashboard(user)
        self.view.close()
        self.dashboard.show()

    def handle_signup(self, form: "SignupForm"):
        signup_data = form.get_data()

        if not form.is_valid_fields():
            return
    
        self._role_selection_view = RoleSelectionView(signup_data)
        self._role_selection_view.show()
        self.view.close()

    def handle_forgot_password(self, form: "ForgotPasswordForm") -> None:
        email = form.get_data()['email']

        if not form.is_valid_fields():
            return

        if not exists_email(email):
            form.email_input.set_state("error")
            return
        
        self.show_verify_code_panel()

    def handle_code_verify(self, form: "VerifyCodeForm") -> None:
        verify_data = form.get_data()

        if not form.is_valid_fields():
            return

        if verify_data['password'] != verify_data['confirm']:
            form.password_input.set_state("error")
            form.confirm_password_input.set_state("error")
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