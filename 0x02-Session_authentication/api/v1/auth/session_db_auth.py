#!/usr/bin/env python3
""" Session Auth Expiration template"""

from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth
# import base64
from typing import TypeVar, Optional
from models.user import User
from uuid import uuid4
from os import getenv
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Session DB class
    """

    def create_session(self, user_id: str = None) -> Optional[str]:
        """ Create a session for a user by generating a"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        kwargs = {
            "user_id": user_id,
            "session_id": session_id,
        }
        user_session_obj = UserSession(**kwargs)
        user_session_obj.save()
        print(user_session_obj.to_json())
        print("Duration: ", self.session_duration)
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> Optional[str]:
        # sourcery skip: aware-datetime-for-utc
        """ Retrieve the user ID associated with a given session ID."""
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return
        # check if its an empty list
        if len(sessions) < 1:
            return

        # get the current time
        current_time = datetime.utcnow()
        # get the current time for our session in seconds as passed
        # in the environmental variable SESSION_TIME
        obj_duration_secs = timedelta(seconds=self.session_duration)
        # get the time left for our session object
        exp_time = sessions[0].created_at + obj_duration_secs

        # check if the time left is less than the current time
        # if it is return None
        if exp_time < current_time:
            return

        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """ Deletes the user session."""
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return False

        if len(sessions) < 1:
            return False

        sessions[0].remove()
        return True
