#!/usr/bin/env python3
"""
expire session demo
"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ expire session class """

    def __init__(self):
        """ initialize objects """

        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ overload create_session """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id, "created_at": datetime.now()}
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ get user_id for session """
        if session_id is None or type(session_id) != str:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict or "created_at" not in session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        tm = self.user_id_by_session_id.get(session_id).get("created_at")
        future = self.user_id_by_session_id.get(session_id).get(
            "created_at") + timedelta(seconds=self.session_duration)
        now = datetime.now()
        if future < now:
            return None
        return self.user_id_by_session_id.get(session_id).get("user_id")
