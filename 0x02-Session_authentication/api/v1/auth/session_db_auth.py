#!/usr/bin/env python3
"""
This module houses the Session storage.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import timedelta, datetime


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
                userSessDict = {
                    'user_id': user_id,
                    'session_id': session_id,
                    }
                userSession = UserSession(**userSessDict)
                userSession.save()
                return session_id
            return None
        return None

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        Returns the user id for a session ID.
        """

        try:
            userIdForSession = UserSession.search({
                'session_id': session_id})

            userIdForSessdict = userIdForSession[0].to_json()

            # check if time was set, if not return the user_id
            if self.session_duration <= 0:
                return userIdForSessdict.get('user_id')

            # get total session time
            userObj = userIdForSession[0]
            session_time = getattr(userObj, 'created_at') + timedelta(
                seconds=self.session_duration)

            if session_time < datetime.now():
                return None

            # if the session is still valid
            return userIdForSessdict.get('user_id')

        except Exception:
            return None

    def destroy_session(self, request=None) -> bool:
        """
        Method to destroy a session.
        """
        if request is None:
            return None

        # request cookies is the session id
        request_cookies = self.session_cookie(request)
        if not request_cookies:
            return False

        userIdForSession = UserSession.search({
                'session_id': request_cookies})

        if not userIdForSession:
            return False
        userIdForSession = userIdForSession[0]
        userIdForSession.remove()
        return True
