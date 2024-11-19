#!/usr/bin/env python3
"""
This module provides a function for hashing
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid

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

    def valid_login(self, email: str, password: str) -> bool:
        """Validate a user login"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False
        except AttributeError:
            return False

    def _generate_uuid(self) -> str:
        """Generate a UUID"""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Create a session for a user
        Args:
            email (str): the user's email
        Returns:
            str: the session token
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None

        if user is None:
            return None

        #Generate new session ID
        session_id = self._generate_uuid()
        try:
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """Get a user from a session ID
        Args:
            session_id (str): the session ID
        Returns:
            str: the user's email
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user.email
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a session
        Args:
            user_id (int): the user's id
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass




