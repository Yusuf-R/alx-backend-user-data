#!/usr/bin/env python3
""" Template for Session Authentication"""
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
    """
    # retrieve the email and password from the request
    email = request.form.get('email')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    # synthesize email and password
    email = email.strip()
    password = password.strip()
    # from the email retrieve the user object
    try:
        user_list = User.search({'email': email})
        print("Hi:  ", user_list)
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(user_list) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    # ensure user object from email matches the password
    for user in user_list:
        if user.is_valid_password(password):
            # create a new session since no session exists
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(getenv('SESSION_NAME'), session_id)
            return response
        else:
            return jsonify({"error": "wrong password"}), 401
