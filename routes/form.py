from flask import Blueprint, request, jsonify, Flask
from flask_mail import Mail, Message
from models.models import db, Users


bot_bh = Blueprint('form', __name__)
app = Flask(__name__)

# Configuration (Replace with your actual credentials)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'selvin472001@gmail.com'
app.config['MAIL_PASSWORD'] = 'eras qjhl eoii mtwg'  # Generate an app-specific password
app.config['MAIL_DEFAULT_SENDER'] = 'selvin472001@gmail.com'

# Initialize Mail
mail = Mail(app)  # Initialize the app with the mail configuration

default_subject = "Default Subject"
default_body = "name, gmail, number, name_of_business"

@bot_bh.route('/send_email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()  # Getting data from the request body
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone')
        name_of_business = data.get('name_of_business')

        # Input validation
        if not name or not email or not phone_number:
            return jsonify({'error': 'Missing parameters'}), 400

        # Create a new user entry in the database
        new_user = Users(name=name, email=email, phone_number=phone_number, name_of_business=name_of_business)
        db.session.add(new_user)
        db.session.commit()

        # Sending email to the user
        user_msg = Message(
            "Registration Confirmation",
            sender=app.config['MAIL_DEFAULT_SENDER'],  # Use default sender
            recipients=[email]
        )
        user_msg.body = f"Dear {name}, thank you for registering!"
        mail.send(user_msg)

        # Sending email to the owner
        owner_msg = Message(
            "New Registration",
            recipients=[app.config['MAIL_DEFAULT_SENDER']]
        )
        owner_msg.body = (
            f"New registration details:\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone Number: {phone_number}\n"
            f"Name of Business: {name_of_business}"
        )
        mail.send(owner_msg)

        return jsonify({'message': 'Emails sent successfully!'}), 200

    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error properly
        return jsonify({'error': 'An error occurred while processing the request.'}), 500
# Register the Blueprint
app.register_blueprint(bot_bh)