import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'tree.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
