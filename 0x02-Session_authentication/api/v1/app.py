#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

# implment an auth instance base on the evn var AUTH-TYPE
if getenv("AUTH_TYPE") == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif getenv("AUTH_TYPE") == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif getenv("AUTH_TYPE") == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()

excluded_paths = [
    '/api/v1/status/',
    '/api/v1/unauthorized/',
    '/api/v1/forbidden/',
    '/api/v1/auth_session/login/',
]

# =========================Task1==============================================
# Error handler: Unauthorized
# What the HTTP status code for a request unauthorized? 401 of course!
# Edit api/v1/app.py:

# Add a new error handler for this status code, the response must be:
# a JSON: {"error": "Unauthorized"}
# status code 401
# you must use jsonify from Flask
# =============================================================================


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


# ================================Task 2=======================================
# Edit api/v1/app.py:
# Add a new error handler for this status code, the response must be:
# a JSON: {"error": "Forbidden"}
# status code 403
# you must use jsonify from Flask
# =============================================================================

@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """ Before request
    """
    if auth is None:
        return
    if auth.require_auth(request.path, excluded_paths) is False:
        return
    if (not auth.authorization_header(request) and
            not auth.session_cookie(request)):
        abort(401)
    if auth.current_user(request) is None:
        abort(403)
    request.current_user = auth.current_user(request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
