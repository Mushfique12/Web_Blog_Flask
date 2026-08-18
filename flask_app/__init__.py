import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Need a Secret Key to protect against modifying cookies and cross-site request forgery attacks
app.config['SECRET_KEY'] = 'a0955833b03a70f5cf8b92852836d83c'
# Sets the location for the Database for the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Creates a DB instance
db = SQLAlchemy(app)
# Encrypts user password
bcrypt = Bcrypt(app)
# Adds login functionality to the app
login_manager = LoginManager(app)
# Sets the login route location (function) for restricted pages that require Login for access
login_manager.login_view = 'login'
# Sets category of the "Login Required" flash message to a built-in Bootstrap class
login_manager.login_message_category = 'info'

# Sets up the email server configuration for sending emails (e.g., for password reset functionality)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

# print(app.config['MAIL_USERNAME'])
# print(app.config['MAIL_PASSWORD'])
mail = Mail(app)

from flask_app import routes