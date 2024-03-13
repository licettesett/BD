import os
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or ' '
    UPLOAD_FOLDER = 'app/static/beats/'
    DB_NAME = 'lr3_ot'
    DB_USER = 'user1'
    USER_PASSWORD = 'parol'
    DB_HOST = 'localhost'
    DB_PORT = 5432