import os

class Config:
    SECRET_KEY = os.urandom(24)
    DATABASE_PATH = 'db/dados.db'
    STATIC_FOLDER = 'static/'
