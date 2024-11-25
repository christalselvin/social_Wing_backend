Social Wynk Registration System
This project is a registration system for Social Wing, a platform designed to help businesses grow and connect. It uses Flask for the backend, integrates email notifications via SMTP, and stores user data in a database.

Features
User registration form with validation.
Database integration for storing user information.
Automated email notifications to users and admin upon registration.
Responsive HTML email template with a logo and social links.
Integration with Flask's static and template directories.

Technologies Used
Python: Core language for backend development.
Flask: Framework for handling routes and templates.
HTML & CSS: For the email template.
PostgreSQL: Database for storing user information.
SMTP (Gmail): For sending automated emails.
Setup Instructions
Prerequisites
Python 3.x
Virtual environment (optional but recommended)
PostgreSQL 
Git (for version control)
Steps
Clone the Repository

bash
Copy code
git clone https://github.com/your-username/social-wynk.git
cd social-wynk
Install Dependencies Create and activate a virtual environment, then install the required packages:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Set Up the Database Configure your database connection in models/models.py:

python
Copy code
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
Then initialize the database:

bash
Copy code
flask db init
flask db migrate
flask db upgrade
Run the Application Start the Flask development server:

bash
Copy code
python run.py
Open the application in your browser at http://127.0.0.1:5000.

API Endpoints
/api/send_email (POST)
Description: Handles user registration and sends confirmation emails.
Request Body: JSON
json
Copy code
{
  "name": "User Name",
  "email": "user@example.com",
  "phone": "1234567890",
  "business": "Business Name"
}
Response:
Success: {"message": "Emails sent and user registered successfully!"}
Error: {"error": "Error message here"}


/api/chatbot (POST)
Description: This endpoint processes user input, determines an appropriate response, and sends back a reply.
Request Body: JSON
json
Copy code
{
  "message": "User's input message here"
}
