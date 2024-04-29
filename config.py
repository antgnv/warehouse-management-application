from database_auth import database_username, database_password, database_host, database_name

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '\xa0\xf1\xf5x\xf7\x137MP\x1f&\xea\x99]\xf5\x12\xbe<X\x07\xa8gY\xe7\xd8\xa7U\xd0\t\xfd_$'
    SQLALCHEMY_DATABASE_URI = f'mysql://{database_username}:{database_password}@{database_host}/{database_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
