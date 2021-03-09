import os


class Config:
    #Configuring app secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')

    #Configuring .db file location. Triple forward slash means CWD
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    #Mail server configuration
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')