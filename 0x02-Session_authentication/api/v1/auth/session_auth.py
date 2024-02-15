#!/usr/bin/env python3
"""
This module is a session authentication module.
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


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
