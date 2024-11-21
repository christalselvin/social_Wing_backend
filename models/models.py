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
    name_of_bussiness = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    def __init__(self, name, name_of_bussiness, email, phone_number):
        self.name = name
        self.name_of_bussiness = name_of_bussiness
        self.email = email
        self.phone_number = phone_number

    def __repr__(self):
        return f"<User {self.name} - {self.name_of_bussiness}>"

