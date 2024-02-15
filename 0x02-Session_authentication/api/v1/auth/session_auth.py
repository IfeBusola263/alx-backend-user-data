#!/usr/bin/env python3
"""
This module is a session authentication module.
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """
    This is a session authentication class which will carry out different
    functions to help with persistence.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        This method creates a Session ID for a user with user id 'user_id'
        Returns None if 'user_id' is None or it is not a string.
        """

        if not user_id or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.__class__.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        This method returns the a User id, based on the session ID,
        'session_id'.
        """

        if not session_id and not isinstance(session_id, str):
            return None

        return self.__class__.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        This method returns a user instances based on the cookies value.
        """

        # check if the there's a request object
        if request:

            # get the session_id from the request cookies
            request_cookies = self.session_cookie(request)

            # Use the session_id to find the user it is mapped to
            if request_cookies:
                user_id = self.user_id_for_session_id(request_cookies)
                return User.get(user_id)
