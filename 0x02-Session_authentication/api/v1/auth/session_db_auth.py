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


class SessionDBAuth(SessionAuth):
    """ Session DB class
    """

    def create_session(self, user_id: str = None) -> str:
        """ Create a session for a user by generating a"""
        return super().create_session(user_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieve the user ID associated with a given session ID."""
        return super().user_id_for_session_id(session_id)

    def destroy_session(self, request=None) -> bool:
        """ Deletes the user session."""
        return super().destroy_session(request)
