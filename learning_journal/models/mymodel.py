import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    )

from .meta import Base

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import(
    scoped_session,
    sessionmaker
    )
from zope.sqlalchemy import ZopeTransactionExtension
from passlib.context import CryptContext
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
password_context = CryptContext(schemes=['pbkdf2_sha512'])

# this is the class that came with the scaffold, we can remove it
# class MyModel(Base):
#     __tablename__ = 'models'
#     id = Column(Integer, primary_key=True)
#     name = Column(Text)
#     value = Column(Integer)
#
#
# Index('my_index', MyModel.name, unique=True, mysql_length=255)

#add entry class - to be used by our learning journal
class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def all(cls, session=None):
        """return a query with all entries, ordered by creation date reversed
        """
        if session is None:
            session = DBSession
        return session.query(cls).order_by(sa.desc(cls.created)).all()

    @classmethod
    def by_id(cls, id, session=None):
        """return a single entry identified by id
        If no entry exists with the provided id, return None
        """
        if session is None:
            session = DBSession
        return session.query(cls).get(id)

# The User class will allow us to authenticate users
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)

    @classmethod
    def by_name(cls, name):
        return DBSession.query(cls).filter(cls.name == name).first()

    def verify_password(self, password):
        return password_context.verify(password, self.password)