from ..exceptions.auth_exceptions import *

from .db import DbResult, DbError

from typing import TypeVar, Literal, NoReturn, overload

"""
The database returns various error descriptors like INVALID_CREDENTIALS,
INVALID_SESSION, etc. which must be translated into a Python exception
that is propagated upwards to be handled by the controller, and then further
displayed to the user where necessary.
"""
ERROR_GROUPS = {
    InvalidCredentialsError: (
        "INVALID_CREDENTIALS",
    ),
    InvalidSessionError: (
        "INVALID_SESSION",
    ),
    UserAlreadyExistsError: (
        "EMAIL_EXISTS",
    ),
    InsufficientPermissionsError: (
        "PENDING_APPROVAL",
        "INSUFFICIENT_PERMISSIONS"
    )
}

# Inverse mapping of the dictionary created above
ERROR_EXC_MAP = {
    code: exc_cls
    for exc_cls, exc_codes in ERROR_GROUPS.items()
    for code in exc_codes
}


T = TypeVar("T")

"""
Necessary for type-correctness, since this function may conditionally raise an
exception based on the `raise_exc` parameter, and thus the return type must be
clarified to the type-checker.
"""
@overload
def unwrap_result(
    result: DbResult[T],
    *,
    raise_exc: Literal[False]
) -> T | None:
    ...


@overload
def unwrap_result(
    result: DbResult[T],
    *,
    raise_exc: Literal[True] = True
) -> T:
    ...


def raise_from_error_t(error: DbError) -> NoReturn:
    """
    Raise an exception from a database error result.

    :param error: the error result returned by the database
    :raises Exception: raises the corresponding exception, if mapped,
                       otherwise Exception
    """
    if error.code is None:
        raise RuntimeError("Result error type had invalid error-code")
    exc_cls = ERROR_EXC_MAP.get(error.code)
    if exc_cls is None:
        raise Exception(
            f"Result returned unhandled error ({error.code}): " +
            f"{error.message!r}"
        )
    raise exc_cls(f"Result returned error: {error.message!r}")


def unwrap_result(result: DbResult[T], *, raise_exc: bool=True) -> T | None:
    """
    Take the result of a database operation and unravel its contents, handling
    any errors as specified by `raise_exc`.

    :param result[T]: the database result
    :param raise_exc: should an exception be raised if the result is an error
                      or return None
    :returns T | None: returns the unwrapped data, None or raises an exception
                       depending on `raise_exc`
    """
    if result.success:
        return result.data
    if not raise_exc:
        return
    if result.error is None:
        raise RuntimeError(
            "Result indicated failure, but no error context provided"
        )
    raise_from_error_t(result.error)