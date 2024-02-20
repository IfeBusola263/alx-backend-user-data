#!/usr/bin/env python3
"""
Flask App for a user application.
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    This method resolves the logout request and invalidates
    the session_id of the user.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
        # return redirect(url_for('home'))
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    This function resolves the request to find a user.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        response = jsonify({"email": user.email})
        return response, 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    This method resolves the request for getting a password reset
    token.
    """

    email = request.form.get('email')
    if email:
        try:
            reset_token = AUTH.get_reset_password_token(email)
            if reset_token:
                return jsonify({"email": email, "reset_token": reset_token})
            abort(403)
        except ValueError:
            abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    This function resolves the request to update the user's
    password, provided the email, reset_token and new_password
    credentials are sent with the request.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    if email and reset_token and new_password:
        try:
            result = AUTH.update_password(reset_token, new_password)
            if result is None:
                return jsonify({"email": email, "message": "Password updated"})
        except ValueError:
            abort(403)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
