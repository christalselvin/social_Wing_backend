from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set up the database URI (make sure to replace it with your database URL)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost/Christal"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)
    name_of_business = db.Column(db.String(100), nullable=True)

    def __init__(self, name, email, phone_number, name_of_business):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.name_of_business = name_of_business
