from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    name_of_business = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<User {self.name}>'


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    content =db.Column(db.String(300),nullable =False)
    data = db.Column(db.LargeBinary, nullable=False)
    mime_type = db.Column(db.String(50), nullable=False)

@staticmethod
def get_details_by_content(content_value):
        """
        Retrieve image details by content.
        :param content_value: The content to search for.
        :return: List of images matching the content.
        """
        return Image.query.filter_by(content=content_value).all()
