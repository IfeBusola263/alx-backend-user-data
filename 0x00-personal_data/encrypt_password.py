#!/usr/bin/env python3
"""
This module demonstrates password encryption.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    This function returns a a salted, hashed password,
    which is a byte string.
    """
    return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    This function checks if a password matches a hashed password
    or not, using bcrypt.
    """

    return bcrypt.checkpw(bytes(password, 'utf-8'), hashed_password)
