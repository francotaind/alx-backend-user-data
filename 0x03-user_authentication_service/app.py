#!/usr/bin/env python3
"""
Basic flask app
"""

from flask import Flask, jsonify, request, abort, make_response
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


@app.route('/sessions', methods=['POST'])
def login():
    """
    Handle user login via POST request.
    Expects for data with 'emeil' and 'password'
    Returns:
    JSON response with user email and login message
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        if not AUTH.valid_login(email, password):
            abort(401)

            session_id = AUTH.create_session(email)

            response = make_response(jsonify({"email": email,
                                              "message": "logged in"}))

            response.set_cookie("session_id", session_id)
            return response
    except Exception:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Handle user logout via DELETE request.
    Expects for data with 'session_id'
    Returns:
    JSON response with user email and logout message
    """
    '#get session ID from cookie'
    session_id = request.cookies.get('session_id')

    '#if no session ID is provided, abort with 403'
    if not session_id:
        abort(403)
    try:
        '#find user by session ID'
        user = AUTH._db.find_user_by(session_id=session_id)

        '#if user is not found, abort with 403'
        if not user:
            abort(403)
        '#Destroy the session by setting session_id to None'
        AUTH._db.update_user(user.id, session_id=None)

        '#Redirect to the homepage'
        return redirect('/')

    except Exception:
        abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
