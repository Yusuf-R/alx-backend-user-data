#!/usr/bin/env python3
""" Session Auth template"""

from api.v1.auth.auth import Auth
# import base64
from typing import TypeVar
from models.user import User
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

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance based on a cookie value.

        Args:
            request (optional): request object that contains the cookie value.

        Returns:
            User instance: The User instance associated with the
            cookie value in the request.
            If the cookie value is invalid or the user does not exist,
            None is returned.
        """
        if request is None:
            return None
        cookie_value = self.session_cookie(request)
        if cookie_value is None:
            return None
        user_id = self.user_id_for_session_id(cookie_value)
        if user_id is None:
            return None
        user_obj = User.get(user_id)
        if user_obj is None:
            return None
        return user_obj

    def destroy_session(self, request=None) -> bool:
        """
        Deletes the user session.

        Args:
            request (optional): A request obj that contains the cookie value.

        Returns:
            bool: True if the session was successfully destroyed,
            False otherwise.
        """
        if request is None:
            return False
        cookie_value = self.session_cookie(request)
        if cookie_value is None:
            return False
        user_id = self.user_id_for_session_id(cookie_value)
        if user_id is None:
            return False
        del self.user_id_by_session_id[cookie_value]
        return True
