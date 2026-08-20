
from flask import Blueprint, render_template, flash, redirect, url_for, request, abort, current_app
from flask_app import db, bcrypt
from flask_app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_app.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

# Need to add the methods to allow GET/POST requests (using the Submit Button)
@users.route("/register", methods=['GET', 'POST'])
def register():
    # Redirects to Home Page is user is logged in correctly
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # Uses the Form to extract the User Input Data
    form = RegistrationForm()
    # Validates the form using the Validators defined in the RegistrationForm class
    if form.validate_on_submit():
        # Hashes the User Password before storing in the Database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Creates an User, and stores in the DB
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # Provides a Flash Message after successful registration. Built-in category for Bootstrap
        flash('Your acccount has been created! You are now able to log in.', 'success')

        return redirect(url_for('users.login'))
    
    # Passes the form parameter to access this form in the HTML template
    return render_template("register.html", title="Register", form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    # Redirects to Home Page if user is logged in correctly
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # Uses the Form to extract the User Input Data
    form = LoginForm()
    # Validates the form using the Validators defined in the LoginForm class
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Validates User email and password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # Gets the next parameter from the url if it exists
            next_page = request.args.get('next')
            
            # Redirects to the next_page or Home Page
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            # Provides a Flash Message after Log in failure. Built-in category for Bootstrap
            flash('Login Unsuccessful. Please check email and password', 'danger')

    # Passes the form parameter to access this form in the HTML template
    return render_template("login.html", title="Login", form=form)

@users.route("/logout")
def logout():
    # Logs the user out
    logout_user()

    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
# Tells the user that Login is required to access this page/route. The login route is specified by "login_view" in the __init__.py file
@login_required
def account():
    # Uses the Form to extract the User Input Data
    form = UpdateAccountForm()
    # Validates the form using the Validators defined in the UpdateAccountForm class
    if form.validate_on_submit():
        # Checks if the user has uploaded a new profile picture
        if form.picture.data:
            # Saves the new profile picture and updates the current user's image_file attribute
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        # Updates the current user's username and email attributes with the new values from the form
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        # Provides a Flash Message after successful account update. Built-in category for Bootstrap
        flash('Your account has been updated!', 'success')

        return redirect(url_for('users.account'))
    
    elif request.method == 'GET':
        # Pre-populates the form fields with the current user's username and email when the page is loaded for the first time
        form.username.data = current_user.username
        form.email.data = current_user.email

    # Generates the URL for the current user's profile picture to be displayed on the account page
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    # Renders the account.html template with the title, image_file, and form parameters
    return render_template("account.html", title="Account", image_file=image_file, form=form)

# Creates the User Posts route to display all posts by a specific user
@users.route("/user/<string:username>")
def user_posts(username):
    # Gets the page number from the query parameters, defaulting to 1 if not provided
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # The query filters the posts by the author (user) and orders them by the date they were posted in descending order. The results are then paginated to show 5 posts per page, based on the current page number.
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=5, page=page)
    return render_template("user_posts.html", posts=posts, user=user)


# Creates the Reset Password Request route to allow users to request a password reset email
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # Redirects to Home Page if user is logged in correctly. Need to log out to reset password
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()

    # Validates the form using the Validators defined in the RequestResetForm class
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Sends the password reset email to the user
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    
    return render_template("reset_request.html", title='Reset Password', form=form)

# Creates the Reset Password route to allow users to reset their password using the token sent in the email
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # Redirects to Home Page if user is logged in correctly. Need to log out to reset password
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Verifies the reset token and retrieves the user associated with it. If the token is invalid or expired, it flashes a message and redirects to the reset request page.
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()

    # Validates the form using the Validators defined in the ResetPasswordForm class
    if form.validate_on_submit():
        # Hashes the new password provided by the user and updates the user's password in the database. After committing the changes, it flashes a success message and redirects to the login page.
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    
    return render_template("reset_token.html", title='Reset Password', form=form)