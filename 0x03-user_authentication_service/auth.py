#!/usr/bin/env python3
"""
This module provides a function for hashing
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


class Auth:
    """Auth class to interact with the auth database
    """
    def __init__(self):
        """Initialize Auth instance"""
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hash a password string using bcrypt

        Args:
            password (str): a string to hash
        Returns:
            bytes: the hashed password
        """
        #convert the password string to bytes
        encoded = password.encode('utf-8')

        #Generate the salt and hash the password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(encoded, salt)
        return hashed

    def register_user(self, email: str, password: str) -> User:
        """Register a user in the database

        Args:
            email (str): the user's email
            password (str): the user's unhashed password
        Returns:
            User: the User object created
        """
        #check if the user exists
        if self._db.find_user_by(email=email) is not None:
            raise ValueError(f'User {email} already exists')

        #If the user doesnt exist create a new one
        hashed_password = self._hash_password(password)
        return self._db.add_user(email, hashed_password)
