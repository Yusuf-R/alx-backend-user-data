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
    
    # Create an instance method def create_session(self, user_id: str = None) -> str:
    # that creates a Session ID for a user_id
    def create_session(self, user_id: str = None) -> str:
        """ create_session """
        if user_id is None or not isinstance(user_id, str):
            return None
        # generate a session_id using uuid4
        session_id = str(uuid4())
        # store the session_id in the user_id_by_session_id dictionary
        self.user_id_by_session_id[session_id] = user_id
        # return session_id
        return session_id
        
    
    # def current_user(self, request=None) -> TypeVar('User'):
    #     """ current_user """
    #     return None
    pass
