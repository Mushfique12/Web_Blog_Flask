from flask import render_template, flash, redirect, url_for, request
from flask_app import app, db, bcrypt
from flask_app.forms import RegistrationForm, LoginForm
from flask_app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2', 
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

# Need to add the methods to allow GET/POST requests (using the Submit Button)
@app.route("/register", methods=['GET', 'POST'])
def register():
    # Redirects to Home Page is user is logged in correctly
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
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

        return redirect(url_for('login'))
    
    # Passes the form parameter to access this form in the HTML template
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    # Redirects to Home Page is user is logged in correctly
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
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
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            # Provides a Flash Message after Log in failure. Built-in category for Bootstrap
            flash('Login Unsuccessful. Please check email and password', 'danger')

    # Passes the form parameter to access this form in the HTML template
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    # Logs the user out
    logout_user()

    return redirect(url_for('home'))

@app.route("/account")
# Tells the user that Login is required to access this page/route. The login route is specified by "login_view" in the __init__.py file
@login_required
def account():
    return render_template("account.html", title="Account")