from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from grand_geckos.database.exceptions import UserAlreadyExistsError
from grand_geckos.database.models import User


class DatabaseWorker:
    engine = create_engine("sqlite:///dbinfo/worker.db", echo=True)

    def __init__(self, user: User):
        self.session = sessionmaker(bind=DatabaseWorker.engine)()
        self.user: User = self.session.query(User).filter_by(username=user.username, password=user.password).first()

    @classmethod
    def create_user(cls, username: str, password: str, password_confirm: str) -> Union[None, User]:
        session = sessionmaker(bind=DatabaseWorker.engine)()
        check_user = session.query(User).filter_by(username=username).first()
        if check_user is not None:
            raise UserAlreadyExistsError("User already exists")
        else:
            user = User(username=username, password=password, password_confirm=password_confirm)
            session.add(user)
            session.commit()
            return cls(user)
