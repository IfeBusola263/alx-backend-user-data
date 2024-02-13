#!/usr/bin/env python3
"""
This is a module for a basic authentication that inherits
from the Auth class.
"""
from api.v1.auth.auth import Auth
from base64 import decodebytes, binascii
from models.user import User
from typing import TypeVar


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        This method returns the decoded value of the Bases 64 string
        'base64_authorization_header'.
        """

        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            byte_rep = base64_authorization_header.encode()
            dcoded = decodebytes(byte_rep)
            return dcoded.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        This method extract the users email and password from the
        'decoded_base64_authorization_header'.
        """

        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email, passwd = decoded_base64_authorization_header.split(':', 1)
        return (email, passwd)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        This method returns a user instance, based on given credentials.
        """

        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        attr = {'email': user_email, '_password': user_pwd}

        # Search for Users data in the storage
        list_of_all_users = User.search({})
        if len(list_of_all_users) == 0:
            return None

        # Search for User based on email
        user_by_email = User.search({'email': user_email})
        if len(user_by_email) == 0:
            return None

        # Validate the password of the user.
        if user_by_email[0].is_valid_password(user_pwd):
            return user_by_email[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        This method validates a users login request with step by step
        authentication, from Auth class.
        """

        # Check for authorization header
        if request is not None:
            auth_value = self.authorization_header(request)

            # Extract the authorization value
            if auth_value is not None:
                b64_val = self.extract_base64_authorization_header(auth_value)

            # decode the value
            if b64_val:
                extracted = self.decode_base64_authorization_header(b64_val)

                # extract authorization information
                if extracted:
                    user_cred = self.extract_user_credentials(extracted)
                    email, passwd = user_cred

                    # validate authorization credentials
                    if email and passwd:
                        return self.user_object_from_credentials(email, passwd)
