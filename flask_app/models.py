from datetime import datetime, timezone
from flask_app import db, login_manager
from flask_login import UserMixin

# Function to reload user from user ID stored in the Database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# SQLAlchemy uses classes (models) for DB structures (tables)
# User Model (class) for a Database Table User (with columns defined as attributes)
# The Login_Manager expects 4 attributes/methods - isAuthenticated, isActive, isAnonymous & getID
# The UserMixin class provides all those
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # Its a relationship, no column is created. It runs an additional Query in the background for all posts the user created
    # Post is capitalized since it refers to the class Post
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# Post Model (class) for Database entry
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    content = db.Column(db.Text, nullable=False)
    # User is small letters cuz it refers to the table name & column name created by User class (default name is the class in lowercase)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
