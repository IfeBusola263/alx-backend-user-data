#!/usr/bin/env python3
"""
This is an authentication module.
"""

from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """
    This method takes a stringed password and uses the bcrypt module
    to encrypt the password 'password', and returns it as bytes.
    """
    return hashpw(bytes(password, 'utf-8'), gensalt())
