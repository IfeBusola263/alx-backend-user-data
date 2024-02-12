#!/usr/bin/env python3
"""
This is a module for a basic authentication that inherits
from the Auth class.
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    This class inherits from the Auth class all methods and attributes
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        This method extracts the Base64 part of the 'authorization_header'
        for a basic authorization.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split()[1]
