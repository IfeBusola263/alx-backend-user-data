#!/usr/bin/env python3
"""
This is the app engine that handles the login authentication.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    This method handles the authentication login.
    """
    email = request.form.get('email')
    pwd = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not pwd:
        return jsonify({"error": "password missing"}), 400

    try:
        user = User.search({'email': email})[0]
        if not user.is_valid_password(pwd):
            return jsonify({"error": "wrong password"}), 401

        from api.v1.app import auth
        user_session_id = auth.create_session(user.id)
        user_cookies_name = getenv('SESSION_NAME')
        response = jsonify(user.to_json())
        response.set_cookie(user_cookies_name, user_session_id)
        return response

    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
