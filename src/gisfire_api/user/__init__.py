import json

from .. import db
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy import func
import random
from sqlalchemy import exc


class User(db.Model):
    __tablename__ = 'user_token'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    token = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    valid_until = Column(DateTime(timezone=True), default=None)
    ts = Column(DateTime(timezone=True), server_default=func.utcnow(), nullable=False)
    access = relationship('UserAccess', back_populates='user', lazy='select')
    CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!()_:;@?"
    TOKEN_LENGTH = 64

    def __init__(self, username, valid_until, is_admin=False):
        """
        TODO:
        :param username:
        :param valid_until:
        :param is_admin:
        """
        self.username = username
        self.valid_until = valid_until
        self.is_admin = is_admin
        self.token = self.get_token(self.TOKEN_LENGTH)

    @staticmethod
    def get_token(length):
        """
        TODO:
        :param length:
        :return:
        """
        token = ""
        for i in range(length):
            token += User.CHARACTERS[random.randint(0, len(User.CHARACTERS) - 1)]
        return token

    class UserJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            """
            JSON Encoder for the USer Object

            :param obj: Object to encode to JSON
            :type obj: Union[User|Object]
            :return:
            """
            if isinstance(obj, User):
                return {
                    'username': obj.username,
                    'valid_until': obj.valid_until.strftime('%Y-%m-%dT%H:%M:%S'),
                    'token': obj.token
                }
            return json.JSONEncoder.default(self, obj)  # pragma: no cover
            # Not testing this code because it is a copy from the python doc. Calling this is an error in the API


class UserAccess(db.Model):
    __tablename__ = 'user_access'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_token.id'))
    ip = Column(postgresql.INET, nullable=False)
    url = Column(String, nullable=False)
    method = Column(String, nullable=False)
    params = Column(String, default=None)
    result_code = Column(Integer, nullable=False)
    ts = Column(DateTime(timezone=True), server_default=func.utcnow(), nullable=False)
    user = relationship('User', back_populates='access')

    def __init__(self, ip, url, method, params=None, user=None, result_code=None):
        """
        TODO:
        :param ip:
        :param url:
        :param method:
        :param params:
        :param user: Union[User|None]
        """
        self.ip = ip
        self.url = url
        self.method = method
        self.result_code = result_code
        self.params = params
        if user is not None:
            self.user_id = user.id
        else:
            self.user_id = None

    def record_access(self, database, result_code=200):
        """
        TODO:

        :param database:
        :param result_code:
        :return:
        """
        try:
            self.result_code = result_code
            database.session.add(self)
            database.session.commit()
        except exc.SQLAlchemyError:  # pragma: no cover
            # No testing of this code because the database error has to be caused by some malfunction of the system.
            # Testing it changing permissions on-the-fly, and other ways cause collateral side effects. If I can perform
            # any other operation just before this access write, there should be som critical error such as a broken
            # connection, internet failure, server failure, etc. So it cannot be tested safely
            db.session.rollback()


