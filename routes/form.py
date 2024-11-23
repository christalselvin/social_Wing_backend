from flask import Blueprint, request, jsonify
from models.models import db, Users
import smtplib

# Define the blueprint
bot_bh = Blueprint('form', __name__)

# Email configuration
SENDER_EMAIL = 'selvin472001@gmail.com'
SENDER_PASSWORD = 'fjcy erhb pkjd gbsd'  # Replace with your app password (not your email password)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

@bot_bh.route('/send_email', methods=['POST'])
def send_email():
    try:
        # Parse the JSON request
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone')
        business = data.get('business')

        # Validate input
        if not name or not email or not phone_number:
            return jsonify({'error': 'Missing required fields: name, email, phone'}), 400

        # Save user to the database
        new_user = Users(name=name, email=email, phone_number=phone_number, business=business)
        db.session.add(new_user)
        db.session.commit()

        # Prepare email content
        subject_user = "Registration Confirmation"
        body_user = f"Dear {name},\n\nThank you for registering with us. We're excited to have you on board!"

        subject_owner = "New Registration Alert"
        body_owner = f"""
        New registration details:
        Name: {name}
        Email: {email}
        Phone Number: {phone_number}
        Business: {business or 'N/A'}
        """

        # Send email to the user
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Email to the user
        message_user = f"Subject: {subject_user}\n\n{body_user}"
        server.sendmail(SENDER_EMAIL, email, message_user)

        # Email to the owner
        message_owner = f"Subject: {subject_owner}\n\n{body_owner}"
        server.sendmail(SENDER_EMAIL, 'owner_email@gmail.com', message_owner)  # Replace with owner's email

        # Close the SMTP connection
        server.quit()

        return jsonify({'message': 'Emails sent and user registered successfully!'}), 200

    except Exception as e:
        # Log and return the error
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
