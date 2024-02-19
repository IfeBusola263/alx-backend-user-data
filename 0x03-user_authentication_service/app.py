#!/usr/bin/env python3
"""
Flask App for a user application.
"""
from flask import Flask, jsonify, request, abort
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """
    This function resolves requests to the home page of the app.
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    This route resolves the user registeration.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({
            "email": email,
            "message": "user created",
        }), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    This Method validates login and sends the session_id as cookie.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    log_stat = AUTH.valid_login(email, password)

    if log_stat:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response

    abort(401)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
