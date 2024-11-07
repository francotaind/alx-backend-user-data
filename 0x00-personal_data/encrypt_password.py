#!/usr/bin/env python3
"""Password encryption using the crypt module."""


import bcrypt


def hash_password(password: str) -> str:
    """Hash a password using the bcrypt algorithm."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
