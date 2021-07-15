from sqlalchemy.exc import ArgumentError


class PasswordMismatch(ArgumentError):
    pass


class UserAlreadyExistsError(ArgumentError):
    pass


class AuthenticationError(ArgumentError):
    pass


class PasswordNotStrongEnough(ArgumentError):
    pass
