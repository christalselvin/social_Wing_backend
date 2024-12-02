import os
from flask import Blueprint, request, jsonify,make_response
from models.models import db, Image

bot_pc = Blueprint('picture', __name__)

@bot_pc.route('/upload/image', methods=['POST'])
def picture_select():
    try:
        # Check if the request contains a file and content field
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        if 'content' not in request.form:
            return jsonify({'error': 'Content field is required'}), 400

        image = request.files['image']
        content = request.form['content']

        # Validate that a file was uploaded
        if image.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Validate the content field length
        if len(content) > 300:
            return jsonify({'error': 'Content exceeds the maximum length of 300 characters'}), 400

        # Check for duplicates in the database
        existing_image = Image.query.filter_by(file_name=image.filename).first()
        if existing_image:
            return jsonify({'error': 'A file with the same name already exists in the database'}), 409

        # Read the image data as binary
        image_data = image.read()
        mime_type = image.content_type

        # Save the image data and content to the database
        new_image = Image(
            file_name=image.filename,
            content=content,
            data=image_data,
            mime_type=mime_type
        )
        db.session.add(new_image)
        db.session.commit()

        return jsonify({'message': 'Image uploaded successfully', 'image_id': new_image.id}), 200

    except Exception as e:
        # Handle unexpected exceptions
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@bot_pc.route('/uploads', methods=['GET'])
def get_images():
    try:
        # Query the database to get all image entries
        images = Image.query.all()

        # Check if there are any images in the database
        if not images:
            return jsonify({'message': 'No images found'}), 404

        # Create a list to hold image details
        image_list = []
        for image in images:
            image_data = {
                'id': image.id,
                'file_name': image.file_name,
                'content': image.content,
                'mime_type': image.mime_type
            }
            image_list.append(image_data)

        return jsonify({'images': image_list}), 200

    except Exception as e:
        # Handle unexpected exceptions
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500