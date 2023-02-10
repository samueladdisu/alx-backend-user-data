#!/urs/bin/env python3
"""
saved session
"""
from models.base import Base


class UserSession(Base):
    """ saved User session """

    def __init__(self, *args: list, **kwargs: dict):
        """ initialize"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
