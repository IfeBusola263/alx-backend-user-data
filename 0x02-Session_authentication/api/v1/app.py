#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
main_paths = [
    '/api/v1/status/',
    '/api/v1/unauthorized/',
    '/api/v1/forbidden/']

if getenv('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif getenv('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def filter_request():
    """
    The request filter checks if an authentication is specified
    in the request, based on the environment variable. Then checks
    if the path is a valid one based on 'main_paths'.
    It then used the 'authorization_header' method of the
    Auth instance to check for the header 'Authorization' if it is
    None or not, the same for 'current_user' method of auth.
    """
    if auth is not None:
        if not auth.require_auth(request.path, main_paths):
            return
        if auth.authorization_header(request) is None:
            abort(401)

        # user_auth gets a User Object if authentication is valid
        user_auth = auth.current_user(request) 
        if user_auth is None:
            abort(403)
        # assign the User object to request.current_user
        request.current_user = user_auth

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authorized(error) -> str:
    """ Handler for unauthorized route
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def is_forbidden(error):
    """
    Handler for the forbidden access.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
