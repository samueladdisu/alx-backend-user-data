#!/usr/bin/env python3
"""
saved session
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ db session """

    def create_session(self, user_id=None):
        """ create new session """
        sid = super().create_session(user_id)
        if sid is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=sid)
        if user_session is None:
            return None
        user_session.save()
        UserSession.save_to_file()
        return sid

    def user_id_for_session_id(self, session_id=None):
        """ set user id """
        if session_id is None or type(session_id) != str:
            return None
        UserSession.load_from_file()
        user_sess = UserSession.search({"session_id": session_id})
        if user_sess is None and user_sess != []:
            return None
        user = user_sess[0]
        if user is None:
            return None
        expired = user.created_at + timedelta(seconds=self.session_duration)
        if expired < datetime.now():
            return None
        return user.user_id

    def destroy_session(self, request=None):
        """ destroy_session """
        if request is None:
            return False
        sid = self.session_cookie(request)
        if sid is None:
            return False
        uid = self.user_id_for_session_id(sid)
        if not uid:
            return False
        session_user = UserSession.search({"session_id": sid})
        if not session_user:
            return False
        try:
            session_user[0].remove()
            UserSession.save_to_file()
        except Exception:
            return False
        return True
