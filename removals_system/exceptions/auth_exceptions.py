class AuthenticationError(Exception):
    """Base class for authentication-related errors."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when login fails due to invalid credentials."""


class UserAlreadyExistsError(AuthenticationError):
    """Raised during signup when the user already exists."""


class InvalidSessionError(AuthenticationError):
    """Raised whenever an invalid session token is passed to a procedure."""


class InsufficientPermissionsError(AuthenticationError):
    """Raised whenever a user has insufficient permissions to perform an action"""