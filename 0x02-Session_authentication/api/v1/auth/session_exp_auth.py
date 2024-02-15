#!/usr/bin/env python3
"""
This module house a class to add expiration to a session.
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    This class implements methods to ensure a login session id
    expires based on lined out constaints.
    """
    def __init__(self):
        """
        Instantiation method for the class.
        This is the first method that run, at the instantiation of
        a SessionExpAuth instance.
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """
        This method uses the super class create_session method.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dictionary = {}
        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.now()
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        This method returns the user id associated with a session_id.
        """
        if not session_id:
            return None

        # get the session dictionary
        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        # check if time was set, if not return the user_id
        if self.session_duration <= 0:
            return session_dict.get('user_id')

        # confirm the session time was recorded
        if not session_dict.get('created_at'):
            return None

        # get total session time
        session_time = session_dict.get('created_at') + timedelta(
            seconds=self.session_duration)

        if session_time < datetime.now():
            return None

        # if the session is still valid
        return session_dict.get('user_id')
