#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar, Dict
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """
        This method creates a user, saves it and returns the user
        object.
        """
        if email and hashed_password:
            # user = User()
            # user.email = email
            # user.hashed_password = hashed_password
            user = User(email=email, hashed_password=hashed_password)
            session = self._session
            session.add(user)
            session.commit()
            # session.close()
            return user

    def find_user_by(self, **kwargs: Dict) -> TypeVar('User'):
        """
        This method finds a user based on the kwargs parameters passed, and
        returns the user.
        A NoResultFound exception is raised if no result is found, while
        A InvalidRequestError is raised if the query has the wrong arguments.
        """

        session = self._session
        try:

            # filtering is achieved with filter_by(), which uses keyword args
            user = session.query(User).filter_by(**kwargs).one()
            return user
        except (NoResultFound, InvalidRequestError) as err:
            raise err

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """
        This method updates a user and returns None on success. If the
        argument passed does not correspond in type, to the users's
        attribute, a value error is raised.
        """

        user = self.find_user_by(id=user_id)

        if user:
            try:
                for key in kwargs:
                    setattr(user, key, kwargs[key])
                session = self._session
                session.commit()
                return None
            except ValueError as err:
                raise err
