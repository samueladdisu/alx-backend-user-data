#!/usr/bin/env python3
"""
session_authentication demo
"""
from uuid import uuid4
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ SessionAuth class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create session """
        if user_id is None:
            return None
        if type(user_id) != str:
            return None
        key = str(uuid4())
        self.user_id_by_session_id[key] = user_id
        return key

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ get user id """
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ get current_user """
        cookie_val = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_val)
        user = User.get(user_id)
        if user:
            self.create_session(user.id)
            return user
        return None

    def destroy_session(self, request=None):
        """ remove session """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        self.user_id_by_session_id.pop(session_id, None)
        return True
