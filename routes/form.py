from flask import Blueprint, request, jsonify, render_template
from models.models import db, Users
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define the blueprint
bot_bh = Blueprint('form', __name__)

# Email configuration
SENDER_EMAIL = 'selvin472001@gmail.com'
SENDER_PASSWORD = 'fjcy erhb pkjd gbsd'  # Replace with your app password (not your email password)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

@bot_bh.route('/api/send_email', methods=['POST'])
def send_email():
    try:
        # Parse the JSON request
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone')
        name_of_business = data.get('business')

        # Validate input
        if not name or not email or not phone_number:
            return jsonify({'error': 'Missing required fields: name, email, phone'}), 400

        # Check if phone number or email already exists in the database
        existing_user = Users.query.filter((Users.phone_number == phone_number) | (Users.email == email)).first()
        if existing_user:
            return jsonify({'error': 'Duplicate phone number or email detected'}), 400

        # Save user to the database
        new_user = Users(name=name, email=email, phone_number=phone_number, name_of_business=name_of_business)
        db.session.add(new_user)
        db.session.commit()

        # Render the HTML email content dynamically
        email_content = render_template(
            'email.html',
            name=name,
            email=email,
            phone_number=phone_number,
            name_of_business=name_of_business
        )

        # Prepare the email for the user
        subject_user = "Registration Confirmation"
        msg_user = MIMEMultipart()
        msg_user['From'] = SENDER_EMAIL
        msg_user['To'] = email
        msg_user['Subject'] = subject_user
        msg_user.attach(MIMEText(email_content, 'html'))

        # Prepare the email for the owner
        subject_owner = "New Registration Alert"
        body_owner = f"""
        New registration details:
        Name: {name}
        Email: {email}
        Phone Number: {phone_number}
        Business: {name_of_business or 'N/A'}
        """
        msg_owner = MIMEMultipart()
        msg_owner['From'] = SENDER_EMAIL
        msg_owner['To'] = 'owner_email@gmail.com'  # Replace with the owner's email
        msg_owner['Subject'] = subject_owner
        msg_owner.attach(MIMEText(body_owner, 'plain'))

        # Send email using SMTP
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send email to the user
        server.sendmail(SENDER_EMAIL, email, msg_user.as_string())

        # Send email to the owner
        server.sendmail(SENDER_EMAIL, 'owner_email@gmail.com', msg_owner.as_string())  # Replace with the owner's email

        # Close the SMTP connection
        server.quit()

        return jsonify({'message': 'Emails sent and user registered successfully!'}), 200

    except Exception as e:
        # Log and return the error
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
