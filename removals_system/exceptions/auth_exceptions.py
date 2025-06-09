class AuthenticationError(Exception):
    """Base class for authentication-related errors."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when login fails due to invalid credentials."""


class UserAlreadyExistsError(AuthenticationError):
    """Raised during signup when the user already exists."""