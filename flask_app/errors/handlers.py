from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

# Error handler for 404 Not Found error. When a user tries to access a page that doesn't exist, this function will be called, and it will render the '404.html' template with a 404 status code.        
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500