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
        # sourcery skip: aware-datetime-for-utc
        """
        Create a session for a user by generating a
        unique session ID using uuid4 and storing it in a dictionary.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.utcnow(),
        }
        self.user_id_by_session_id[session_id] = session_dict
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
        # finding the time delta of the session

        # this will be the record of the querry time
        current_datetime = datetime.utcnow()

        # get the current time for our session in seconds as passed
        # in the environmental variable SESSION_TIME
        obj_duration_secs = timedelta(seconds=self.session_duration)

        # calculate the available time of the object session
        # this will be cobinint the time the object was created and the
        # expiration time value given to the object at instantiation
        available_time = session_dict['created_at'] + obj_duration_secs

        # we compare if the available time is less than the current time
        # if it is less, that means it has expired already

        # evaluat the time left for our session object
        if available_time < current_datetime:
            return None
        return session_dict['user_id']
