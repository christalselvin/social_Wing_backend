import  os
from flask import Blueprint,request,jsonify

bot_lh =  Blueprint('login',__name__)


@bot_lh.route('/api/login', methods=['POST'])
def login():
    try:
        # Parse JSON request data
        data = request.get_json()

        # Validate data and check credentials
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing username or password'}), 400

        username = data.get('username')
        password = data.get('password')

        if username == 'aswin' and password == 'socialwing@02':
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Login failed. Please check your credentials.'}), 401

    except Exception as e:
        # Handle unexpected exceptions
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500




