#!/usr/bin/env python3
"""
This is a User model created from an ORM (sqlalchemy).
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column


Base = declarative_base()


class User(Base):
    """
    This is the user class which users instance would be
    created from, to be store in the database.
    """

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250))
