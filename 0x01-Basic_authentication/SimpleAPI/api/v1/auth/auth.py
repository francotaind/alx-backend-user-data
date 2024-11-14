#!/usr/bin/env python3
"""Auth module for the API"""


from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns True if the path is not in the list of excluded_paths
        Args:
            path (str): the path to check
            excluded_paths (List[str]): the list of paths that should be excluded
        Returns:
            bool: True if the path is not in the list of excluded_paths
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        """Ensure path ends with '/' for consistent comparison"""
        path = path + '/' if not path.endswith('/') else path

        for excluded_path in excluded_paths:
            if excluded_path.endswith('/'):
                if path == excluded_path:
                    return False
            else:
                if path == excluded_path + '/':
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the Authorization header from the request
        Args:
            request: Flask request object
        Returns:
            Authorization header value or None
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None - request is not implemented"""
        return None

