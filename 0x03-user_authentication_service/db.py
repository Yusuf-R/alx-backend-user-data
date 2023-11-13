#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    # Implement the add_user method, which has two required string arguments:
    # email and hashed_password, and returns a User object.
    # The method should save the user to the database.
    # No validations are required at this stage.
    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user with the given email and hashed password.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created user.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    # In this task you will implement the DB.find_user_by method.
    # This method takes in arbitrary keyword arguments and returns
    # the first row found in the users table as filtered by the method’s input arguments. # noqa: E501
    # Make sure that SQLAlchemy’s NoResultFound and InvalidRequestError
    # are raised when no results are found, or when wrong query
    # arguments are passed, respectively.

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by the given criteria.

        Args:
            **kwargs: The criteria to search for a user.

        Returns:
            User: The user that matches the given criteria.

        Raises:
            InvalidRequestError: If no criteria is provided.
            NoResultFound: If no user is found that matches the given criteria.
        """
        if kwargs is None:
            raise InvalidRequestError
        result = self._session.query(User).filter_by(**kwargs).first()
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user by the given criteria.
        """
        # Implement DB.update_user method that takes as argument a required
        # user_id integer and arbitrary keyword arguments, and returns None.
        # The method will use find_user_by to locate the user to update,
        # then will update the user’s attributes as passed in the
        # method’s arguments then commit changes to the database.
        # If an argument that does not correspond to a user
        # attribute is passed, raise a ValueError.
        user = self.find_user_by(id=user_id)
        if user is None:
            raise ValueError
        for key, value in kwargs.items():
            if key in user.__dict__:
                setattr(user, key, value)
            else:
                raise ValueError
        self._session.commit()
        return None
