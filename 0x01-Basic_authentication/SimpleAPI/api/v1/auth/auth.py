#!/usr/bin/env python3
"""
API Authentication handler to manage access to app resources.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    This class manages all the authentication methods and responses.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns True if path is allowed and false otherwise.
        """
        return False

    def authorization_header(self, request: request = None) -> str:
        """
        Returns None for the time being.
        """
        return None

    def current_user(self, request: request = None) -> TypeVar('User'):
        """
        Returns None for the time being.
        """
        return None
