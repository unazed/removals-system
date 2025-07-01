from ..exceptions.auth_exceptions import *

from .db import DbResult, DbError

from typing import TypeVar, Literal, NoReturn, overload


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

ERROR_EXC_MAP = {
    code: exc_cls
    for exc_cls, exc_codes in ERROR_GROUPS.items()
    for code in exc_codes
}


T = TypeVar("T")

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
    if result.success:
        return result.data
    if not raise_exc:
        return
    if result.error is None:
        raise RuntimeError(
            "Result indicated failure, but no error context provided"
        )
    raise_from_error_t(result.error)