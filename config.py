import os

class Config:
    SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tree.db'  # Use tmp directory for Render compatibility
    SQLALCHEMY_TRACK_MODIFICATIONS = False

