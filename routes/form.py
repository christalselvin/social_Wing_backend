from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from importlib.resources import Resource
from urllib.parse import urlparse
from functools import wraps
from flask import current_app as app
from models.models import db,Users


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'selvin472001@gmail.com'  # Enter your Gmail address
app.config['MAIL_PASSWORD'] = 'jbkw gjgy daei jyub'     # Enter your app-specific password
app.config['MAIL_DEFAULT_SENDER'] = 'selvin472001@gmail.com'

mail = Mail(app)

default_subject = "Default Subject"
default_body = "name","gmail","number"

@app.route('/send_email', methods=['POST'])
def send_email():
    try:

        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone')

        if not name or not email or not phone_number:
            return jsonify({'error': 'Missing parameters'}), 400

        new_user = Users(name=name, email=email, phone_number=phone_number)
        db.session.add(new_user)
        db.session.commit()

        user_msg = Message("Registration Confirmation", recipients=[email])
        user_msg.body = f"Dear {name}, thank you for registering!"

        owner_msg = Message("New Registration", recipients=["owner_email@gmail.com"])
        owner_msg.body = f"New registration details:\nName: {name}\nEmail: {email}\nPhone Number: {phone_number}"

        mail.send(user_msg)
        mail.send(owner_msg)

        return jsonify({'message': 'Emails sent successfully!'})
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 500