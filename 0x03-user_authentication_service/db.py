#!/usr/bin/env python3
"""DB module."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session

from user import Base, User

class DB:
    """DB class."""

    def __init__(self) -> None:
        """
        Initialize a new DB instance.
        """
        self._engine = create_engine('sqlite:///a.db', echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session


    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a user to the database.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by a given attribute.
        """
        try :
            return self._session.query(User).filter_by(**kwargs).first()
        except:
            raise InvalidRequestError()

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        update a user's attr in the database
            Args:
                user_id: int
                kwargs: dict
            Raises:
                ValueError: if an invalid attr is passed
        """
        user = self.find_user_by(id=user_id)

        for key in kwargs:
            if not hasattr(User, key):
                raise ValueError(f'Invalid user attribute: {key}')

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
