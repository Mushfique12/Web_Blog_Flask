from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_app.config import Config

# Creates a DB instance
db = SQLAlchemy()
# Encrypts user password
bcrypt = Bcrypt()
# Adds login functionality to the app
login_manager = LoginManager()
# Sets the login route location (function) for restricted pages that require Login for access
login_manager.login_view = 'users.login'
# Sets category of the "Login Required" flash message to a built-in Bootstrap class
login_manager.login_message_category = 'info'
# Sets up the email server configuration for sending emails (e.g., for password reset functionality)
mail = Mail()


# Factory function to create the Flask application instance
def create_app(config_class=Config):
    # Create the Flask application instance
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Import and register blueprints for different parts of the application
    from flask_app.main.routes import main as main_blueprint
    from flask_app.posts.routes import posts as posts_blueprint
    from flask_app.users.routes import users as users_blueprint
    from flask_app.errors.handlers import errors as errors_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(errors_blueprint)

    return app