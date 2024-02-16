#!/usr/bin/env python3
"""
This moudle is a session handler for syoring sessions even when the
app stops.
"""
from models.base import Base


class UserSession(Base):
    """
    This class handles the session storage of users.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        This is the first method that runs after the instace of
        the class is created.
        """
        # super().__init__(*args, **kwargs)
        self.user_id: str = kwargs.get('user_id')
        self.session_id: str = kwargs.get('session_id')
