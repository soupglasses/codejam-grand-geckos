from sqlalchemy.exc import ArgumentError


class PasswordMismatch(ArgumentError):
    pass


class UserAlreadyExistsError(ArgumentError):
    pass
