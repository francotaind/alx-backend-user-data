#!/usr/bin/env python3
"""
Basic flask app
"""

from flask import Flask, jsonify, request
from auth import Auth
AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """Return Welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """To register a new user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "User already exists"}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
