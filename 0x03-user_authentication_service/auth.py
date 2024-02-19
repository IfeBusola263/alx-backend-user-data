#!/usr/bin/env python3
"""
This is an authentication module.
"""

from bcrypt import hashpw, gensalt
from db import DB
from typing import TypeVar
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    This method takes a stringed password and uses the bcrypt module
    to encrypt the password 'password', and returns it as bytes.
    """
    return hashpw(bytes(password, 'utf-8'), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        The first method called at the instantiation of the class.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """
        This method registers a new user.
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
