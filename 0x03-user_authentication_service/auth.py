#!/usr/bin/env python3
""" Auth template"""

from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """
        Hash the given password using bcrypt.hashpw.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
    # In this task you will define a _hash_password method
    # that takes in a password string arguments and returns bytes.
    # The returned bytes is a salted hash of the input password,
    # hashed with bcrypt.hashpw.
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Initialize a new Auth instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
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
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Login a user in the authentication database.

        Args:
            email (str): The email of the user to be logged in.
            password (str): The password of the user to be logged in.

        Returns:
            str: Returns True if the provided email and password.
                 Returns False if the provided email and password.
        """
        try:
            user = self._db.find_user_by(email=email)
            # this will return true or false depending on the outcome
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)  # noqa: E501
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """Generate a new UUID.

        Returns:
            str: A string representing a new UUID.
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """
        Create a new session for the user.

        Args:
            email (str): The email of the user to create a new session for.

        Returns:
            str: The session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Get a user from a session ID.

        Args:
        session_id (str): The session ID.

        Returns:
        User: The corresponding user.
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a session for a user.
        """
        # can be achieved by setting session_id to None for the user object
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset password token for a user.
        """
        if email is None or not isinstance(email, str):
            raise ValueError from None
        try:
            user = self._db.find_user_by(email=email)
            reset_token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError from None

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update a user password.
        """
        if reset_token is None or not isinstance(reset_token, str):
            raise ValueError from None
        if password is None or not isinstance(password, str):
            raise ValueError from None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = self._db._hash_password(password)
            self._db.update_user(user.id, reset_token=None,
                                 hashed_password=hashed_password)
            return None
        except NoResultFound:
            raise ValueError from None
