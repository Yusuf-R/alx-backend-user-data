#!/usr/bin/env python3
""" Session Auth Expiration template"""

from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth
# import base64
from typing import TypeVar
from models.user import User
from uuid import uuid4
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Session Auth Expiration class
    """

    def __init__(self) -> None:
        super().__init__()
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session for a user by generating a
        unique session ID using uuid4 and storing it in a dictionary.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve the user ID associated with a given session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        # for simplicity create a dict called session_dict
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict['user_id']
        if 'created_at' not in session_dict:
            return None
        # finding the time delta
        created_at = datetime.now()
        duration = timedelta(seconds=self.session_duration)
        expiration_time = session_dict['created_at'] + duration
        if expiration_time < created_at:
            return None
        return session_dict['user_id']
