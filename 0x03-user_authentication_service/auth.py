#!/usr/bin/env python3
"""
This is an authentication module.
"""

from bcrypt import hashpw, gensalt, checkpw
from db import DB
from typing import TypeVar, Union
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    This method takes a stringed password and uses the bcrypt module
    to encrypt the password 'password', and returns it as bytes.
    """
    return hashpw(bytes(password, 'utf-8'), gensalt())


def _generate_uuid() -> str:
    """
    This method generates a uuid and returns it.
    """
    return str(uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        This method checks if a user is logging in with valid credentials.
        Returns True if the credentials are right and False otherwise.
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            return checkpw(
                bytes(password, 'utf-8'), existing_user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        This method returns a session ID.
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(existing_user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(
            self, session_id: str) -> Union[TypeVar('User'), None]:
        """
        This method gets a user through the session id and returns the
        user object. If the session id is invalid, it returns None.
        """

        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                return None

        return None

    def destroy_session(self, user_id: int) -> None:
        """
        This method invalidates a users session_id.
        """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        This method sets the reset_token attribute of the user in
        the database.
        """
        if email:
            try:
                user = self._db.find_user_by(email=email)
                reset_token = _generate_uuid()
                self._db.update_user(user.id, reset_token=reset_token)
                return reset_token
            except NoResultFound:
                raise ValueError

        return None

    def update_password(self, reset_token: str, password: str) -> None:
        """
        This method updates the user's password, provided the given
        credentials reset_token and password are accurate, based on the
        database values.
        Returns None.
        """
        if reset_token:
            try:
                user = self._db.find_user_by(reset_token=reset_token)
                hashed_password = _hash_password(password)
                self._db.update_user(
                    user.id, hashed_password=hashed_password, reset_token=None)
                return None
            except NoResultFound:
                raise ValueError
