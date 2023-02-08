#!/usr/bin/env python3
"""
Basic Authentication
"""
from flask import request
from typing import List, TypeVar, Optional


class Auth:
    """ Authentication Class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ decorator to make sure logged in """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != "/":
            path += "/"
        if path.startswith(excluded_paths[0][:excluded_paths[0].index("*")]):
            return False
        return True

    def authorization_header(self, request=None) -> Optional[str]:
        """ authorization_header """
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """ get current logged in user """
        return None
