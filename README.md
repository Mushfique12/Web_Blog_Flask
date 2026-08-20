# Web Blog Flask

A Flask blog application with user authentication, account management, password
reset emails, profile pictures, and CRUD operations for blog posts.

## Features

- User registration and login
- Password hashing with Flask-Bcrypt
- Login-protected account and post-management pages
- Create, read, update, and delete blog posts
- Paginated home and user-post pages
- Profile picture uploads and resizing
- Password reset email workflow
- Custom 403, 404, and 500 error pages
- Modular Flask Blueprints

## Technology

- Python
- Flask
- Flask-SQLAlchemy with SQLite or another configured database
- Flask-Login
- Flask-Bcrypt
- Flask-WTF and WTForms
- Flask-Mail
- Jinja2
- Pillow

## Setup

### 1. Clone or download the project

Open a terminal in the project directory:

```powershell
cd Web_Blog_Flask
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root. The following variables are used by
`flask_app/config.py`:

```env
SECRET_KEY=replace-with-a-long-random-secret
SQLALCHEMY_DATABASE_URI=sqlite:///site.db
EMAIL_USER=your-email@example.com
EMAIL_PASS=your-email-password-or-app-password
```

Do not commit `.env` or real credentials. For Gmail SMTP, an app password may
be required when two-factor authentication is enabled.

## Database

The application uses Flask-SQLAlchemy. To create the database tables, run:

```powershell
python
```

Then, in the Python shell:

```python
from flask_app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
```

## Running the application

From the project root:

```powershell
python run.py
```

The development server is available at:

```text
http://127.0.0.1:5000
```

`run.py` starts Flask in debug mode for local development. Do not use debug
mode in production.

## Project structure

```text
Web_Blog_Flask/
├── flask_app/
│   ├── config.py              # Environment-based configuration
│   ├── models.py              # User and Post database models
│   ├── errors/                # Error handlers and templates
│   ├── main/                  # Home and About blueprints
│   ├── posts/                 # Post routes and PostForm
│   ├── users/                 # Authentication, account, and reset routes/forms
│   ├── static/                # CSS and profile pictures
│   └── templates/              # Jinja2 templates
├── requirements.txt
├── run.py
└── .env                       # Local configuration; not committed
```

## Blueprint endpoints

Application routes are organized under these blueprint names:

- `main.home`, `main.about`
- `posts.new_post`, `posts.post`, `posts.update_post`, `posts.delete_post`
- `users.register`, `users.login`, `users.logout`, `users.account`
- `users.user_posts`, `users.reset_request`, `users.reset_token`

Use the qualified endpoint names in templates and redirects, for example:

```jinja2
{{ url_for('posts.post', post_id=post.id) }}
```

## Security notes

- Use a unique production `SECRET_KEY`.
- Keep SMTP credentials and other secrets out of source control.
- Configure a production WSGI server and disable Flask debug mode before
  deployment.
