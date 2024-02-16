#!/usr/bin/env python3
"""
This module houses the Session storage.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    This is the session storage class to archive all sessions from users.
    """
    def create_session(self, user_id=None) -> str:
        """
        Creates and stores new instance of storage and returns
        the session id.
        """
        if user_id:
            session_id = super().create_session(user_id)
            if session_id:

                userSession = UserSession(**self.user_id_by_session_id)
                userSession.save()
                return session_id
            return None
        return None

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        Returns the user for a session ID.
        """
        try:
            userIdForSession = UserSession.search({
                'session_id': session_id})
            userIdForSession = userIdForSession.to_json()
            return userIdForSession.get('user_id')
        except Exception:
            return None

    def destroy_session(self, request=None) -> bool:
        """
        Method to destroy a session.
        """
        pass
