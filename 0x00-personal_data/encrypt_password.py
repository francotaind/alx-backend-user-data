#!/usr/bin/env python3
"""
Password Encryption and Validation Module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and returns the hashed password."""
    # Generate a salt
    salted = bcrypt.gensalt()
    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salted)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
