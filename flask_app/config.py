import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Need a Secret Key to protect against modifying cookies and cross-site request forgery attacks
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Sets the location for the Database for the app
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # Sets up the email server configuration for sending emails (e.g., for password reset functionality)
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')