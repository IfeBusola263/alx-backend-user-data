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
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        # Make the method slash tolerant
        # if path[-1] == '*':
        #     path = path
        if path[-1] != '/':
            path = path + '/'

        # check if path is in excluded_paths
        if path not in excluded_paths:
            return True

        return False

    def authorization_header(self, request: request = None) -> str:
        """
        Returns None for the time being.
        """
        if request is None:
            return request

        header_value = request.headers.get('Authorization')
        return header_value

    def current_user(self, request: request = None) -> TypeVar('User'):
        """
        Returns None for the time being.
        """
        return None
