from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import relationship

Base: DeclarativeMeta = declarative_base()


class User(Base):
    """Class representing a local user of the 'Secret Crate of Grand Geckos'."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    salt = Column(String)
    credentials_id = relationship("credentials")
    last_login = Column(DateTime)


class Credential(Base):
    """Class representing a credential of a local user of the 'Secret Crate of Grand Geckos'."""

    __tablename__ = "credentials"
    id = Column(Integer, primary_key=True)
    credential_name = Column(String)
    credential_username = Column(String)
    credential_password = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    platform = relationship("Platform", back_populates="credential")


class Platform(Base):
    """Class representing a Platform that can be added to the 'Secret Crate of Grand Geckos'."""

    __tablename__ = "platforms"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    credential = relationship("Credential", back_populates="platforms")
