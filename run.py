from flask_app import create_app

app = create_app()

# Run the Flask application in debug mode when this script is executed directly. This allows for automatic reloading of the server on code changes and provides detailed error messages.
if __name__ == "__main__":
    app.run(debug=True)