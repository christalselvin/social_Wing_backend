from flask import Blueprint, request, jsonify
from models.models import db, Users
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define the blueprint
bot_bh = Blueprint('form', __name__)

# Email configuration
SENDER_EMAIL = 'socialwing02@gmail.com'
SENDER_PASSWORD = 'qhpt uslr uwfv dgzw'  # Replace with your app password (not your email password)
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

        # Prepare HTML email content with CSS
        subject_user = "Registration Confirmation"
        body_user = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Registration Confirmation</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                }}

                .email-container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    position: relative;
                }}

                .email-wrapper {{
                    background-size: cover;
                    background-position: center;
                    padding: 20px;
                }}

                h1 {{
                    color: #1a73e8;
                    margin-top: 20px;
                }}

                p, li {{
                    font-size: 16px;
                    line-height: 1.6;
                    margin: 10px 0;
                }}

                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    font-size: 12px;
                    color: #777;
                }}

                a {{
                    font-weight: 800;
                    text-decoration: none;
                }}

                a:hover {{
                    text-decoration: underline;
                }}

                .social-links {{
                    display: flex;
                    justify-content: center;
                    gap: 10px;
                }}

                .whatsapp-icon {{
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                }}

                .social-icon {{
                    font-size: 20px;
                    color: #1a73e8;
                }}
            </style>
        </head>
        <body>
            <div class="email-wrapper">
                <div class="email-container">
                    <h1>Dear {name},</h1>

                    <p>Thank you for registering with Social Wynk! We're excited to have you on board.</p>

                    <p>Your registration has been successfully received, and we're looking forward to helping you grow your business and connect with others through our platform.</p>

                    <p>Here are the details we received:</p>
                    <ul>
                        <li><strong>Name:</strong> {name}</li>
                        <li><strong>Email:</strong> {email}</li>
                        <li><strong>Phone Number:</strong> {phone_number}</li>
                        <li><strong>Business:</strong> {name_of_business if name_of_business else 'N/A'}</li>
                    </ul>

                    <div class="footer">
                        <p>If you have any questions or need further assistance, feel free to reach out to us. We're here to help!</p>
                        <p>Best regards,</p>
                        <p>The Social Wing Team</p>
                        <p class="whatsapp-icon">
                            <i class="fab fa-whatsapp" style="font-size: 33px; color: #25D366;"></i>
                            <a href="https://wa.me/9789647901" class="whatsapp-link" style="color:#00fb1f;">Whatsapp now</a>
                        </p>

                        <div class="social-links">
                            <a href="https://www.instagram.com/socialwingads?igsh=djA5OTdxbGQ0cjBr" class="social-icon">
                                <i class="fab fa-instagram" style="font-size: 33px;"></i>
                            </a>
                            <a href="https://www.facebook.com/share/1EUJyeNzAW/?mibextid=LQQJ4d" class="social-icon">
                                <i class="fab fa-facebook-f" style="font-size: 33px;"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        subject_owner = "New Registration Alert"
        body_owner = f"""
        New registration details:
        Name: {name}
        Email: {email}
        Phone Number: {phone_number}
        Business: {name_of_business or 'N/A'}
        """

        # Create message container for user email
        msg_user = MIMEMultipart()
        msg_user['From'] = SENDER_EMAIL
        msg_user['To'] = email
        msg_user['Subject'] = subject_user
        msg_user.attach(MIMEText(body_user, 'html'))

        # Create message container for owner email
        msg_owner = MIMEMultipart()
        msg_owner['From'] = SENDER_EMAIL
        msg_owner['To'] = 'owner_email@gmail.com'  # Replace with owner's email
        msg_owner['Subject'] = subject_owner
        msg_owner.attach(MIMEText(body_owner, 'plain'))

        # Send email using SMTP
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send email to the user
        server.sendmail(SENDER_EMAIL, email, msg_user.as_string())

        # Send email to the owner
        server.sendmail(SENDER_EMAIL, 'owner_email@gmail.com', msg_owner.as_string())  # Replace with owner's email

        # Close the SMTP connection
        server.quit()

        return jsonify({'message': 'Emails sent and user registered successfully!'}), 200

    except Exception as e:
        # Log and return the error
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
