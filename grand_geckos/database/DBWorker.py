from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import Union

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from grand_geckos.database.exceptions import (
    AuthenticationError,
    PasswordMismatch,
    PasswordNotStrongEnough,
    UserAlreadyExistsError,
)
from grand_geckos.database.models import Credential, User
from grand_geckos.utils.password_checker import check_password


class DatabaseWorker:
    """A class that creates a connection between the DB Layer and UI layer"""

    engine = create_engine("sqlite:///worker.db")

    def __init__(self, user: User):
        self.session = sessionmaker(bind=DatabaseWorker.engine)()
        self.user: User = self.session.query(User).filter_by(id=user.id).first()

    @classmethod
    def create_user(cls, username: str, password: str, password_confirm: str) -> Union[None, User]:
        """Returns a new DatabaseWorker instance with the newly registered user if every check passes"""
        if password != password_confirm:
            raise PasswordMismatch("Passwords must match!")
        session = sessionmaker(bind=DatabaseWorker.engine)()
        check_user = session.query(User).filter_by(username=username).first()
        password_strength = check_password(password)
        if check_user is not None:
            raise UserAlreadyExistsError("User already exists")
        elif password_strength:
            raise PasswordNotStrongEnough(
                "Password is not strong enough! \n -" + "\n -".join([str(issue) for issue in password_strength])
            )
        else:
            user = User(username=username, password=password, password_confirm=password_confirm)
            session.add(user)
            session.commit()
            return cls(user)

    def vault_key(self, user: User, password: str) -> Fernet:
        salt = urlsafe_b64decode(user.salt)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=10000)
        key = urlsafe_b64encode(kdf.derive((password.encode("utf-8"))))
        f = Fernet(key)
        return f

    def delete_user(self) -> None:
        """Deletes the current logged in user and terminates the session"""
        self.session.query(User).filter_by(id=self.user.id).delete()
        del self.user
        self.session.close()
        del self.session

    def append_credential(self, cred: Credential) -> None:
        self.user.credentials.append(cred)
        self.session.commit()

    @classmethod
    def auth_user(cls, username: str, password: str) -> Union[None, User]:
        """
        Authenticates the user, if the credentials are correct returns a DatabaseWorker instance with the user

        Otherwise, it raises an AuthenticationError
        """
        session = sessionmaker(bind=DatabaseWorker.engine)()
        user = session.query(User).filter_by(username=username).first()
        if user is None:
            raise AuthenticationError("User does not exists!")
        salt = urlsafe_b64decode(user.salt)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=10000)
        key = urlsafe_b64encode(kdf.derive((password.encode("utf-8"))))
        f = Fernet(key)
        if f.decrypt(user.password.encode("utf-8")).decode("utf-8") == password:
            return cls(user=user)
        else:
            raise AuthenticationError("Wrong password, or username.")

    def list_credentials(self):
        return self.user.credentials
