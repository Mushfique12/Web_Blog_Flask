import os
import secrets
from PIL import Image
from flask import url_for, current_app as app
from flask_mail import Message
from flask_app import mail

# Function to resize & save the profile picture uploaded by the user
def save_picture(form_picture):
    # Generates a random hex to avoid filename conflicts and maintain uniqueness
    random_hex = secrets.token_hex(8)
    # Splits the filename into name and extension - the extension is needed to save the file in the correct format
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # Creates the path to save the profile picture in the static/profile_pics directory
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Resize the image to a smaller size to save space and improve performance
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

# Function to send a password reset email to the user
def send_reset_email(user):
    # Generates a password reset token for the user using the get_reset_token method defined in the User model
    token = user.get_reset_token()
    # Creates a new email message with the subject, sender, and recipient information. The sender is set to 'noreply@blog.com'
    msg = Message('Password Reset Request',
                   sender=("My App", "noreply@example.com"),
                   recipients=[user.email])
    # Sets the body of the email message to include the password reset link with the generated token
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    # Sends the email message using the mail instance
    mail.send(msg)