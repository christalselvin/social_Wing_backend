from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.chatbot import bot_bp
from flask_mail import Mail
from routes.form import bot_bh
from models.models import db
from flask_cors import CORS  # Import CORS

def create_app():
    # Create the Flask app instance
    app = Flask(__name__)

    # Enable CORS for all routes (you can also specify origins or other options if needed)
    CORS(app)

    # Load configurations
    app.config.from_object('config.config')

    # Configuration for SQLAlchemy and Mail (if needed)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost/Christal"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the db object and Mail (optional, for email functionality)
    db.init_app(app)

    # Create database tables if not already created
    with app.app_context():
        db.create_all()

    # Register blueprints with the app
    app.register_blueprint(bot_bp)
    app.register_blueprint(bot_bh)

    # Initialize the Mail extension
    mail = Mail(app)

    return app

# Main entry point for the application
if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
