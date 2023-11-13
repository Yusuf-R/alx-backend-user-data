#!/usr/bin/env python3
""" Auth template"""

from db import DB
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Initialize a new Auth instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> None:
        """Register a new user in the authentication database.

        Args:
            email (str): The email of the user to be registered.
            password (str): The password of the user to be registered.

        Raises:
            ValueError: If the email or password is None,
            or if the user already exists in the database.

        Example Usage:
            auth = Auth()
            auth.register_user("example@example.com", "password123")
        """
        if email is None:
            raise ValueError("email cannot be None")
        if password is None:
            raise ValueError("password cannot be None")
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            self._db.add_user(email, self._db._hash_password(password))