#!/usr/bin/env python3
""" Session Auth template"""

from api.v1.auth.auth import Auth
# import base64
# from typing import TypeVar
# from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """ Session Auth class
    """
    # class attribute user_id_by_session_id
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session for a user by generating a
        unique session ID using uuid4 and storing it in a dictionary.

        Args:
            user_id (str, optional): A string representing the user ID.

        Returns:
            str: A string representing the generated session ID.

        Example Usage:
            # Initialize the SessionAuth class object
            session_auth = SessionAuth()

            # Create a session for a user with user ID '123'
            session_id = session_auth.create_session('123')
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        # generate a session_id using uuid4
        session_id = str(uuid4())
        # store the session_id in the user_id_by_session_id dictionary
        self.user_id_by_session_id[session_id] = user_id
        # return session_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve the user ID associated with a given session ID.

        Args:
            session_id: A string representing the session ID.

        Returns:
            str: The user ID associated with the given session ID.
                If the session ID does not exist, None is returned.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        if session_id in self.user_id_by_session_id:
            return self.user_id_by_session_id.get(session_id)
        return None

    # def current_user(self, request=None) -> TypeVar('User'):
    #     """ current_user """
    #     return None
    pass
