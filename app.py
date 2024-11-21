from flask import Flask
from routes.chatbot import bot_bp
# from routes.form import bot_bh

def create_app():
    # Create the Flask app instance
    app = Flask(__name__)

    # Register the blueprint with the app
    app.register_blueprint(bot_bp)
    # app.register_blueprint(bot_bh)


    return app

# Main entry point for the application
if __name__ == '__main__':
    db.create_all()
    app = create_app()
    app.run(host ="0.0.0.0",port=5000)  # Run the app in debug mode
