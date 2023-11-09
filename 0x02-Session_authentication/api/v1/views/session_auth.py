#!/usr/bin/env python3
""" Template for Session Authentication"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Handle the POST request to the '/auth_session/login'
    endpoint for user authentication.

    Args:
        None

    Returns:
        str: JSON representation of the user object and
                sets a session ID cookie if successful.
             JSON response with an error message and status code 400
                if the email or password is missing or empty.
             JSON response with an error message and status code 404
                if no user is found for the provided email.
             JSON response with an error message and status code 401
                if the password is incorrect.
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
    # from the email retrieve the list of user object with such email
    try:
        user_obj_list = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(user_obj_list) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    # from the list of obj, extract the user_obj
    # that fits the password
    for user_obj in user_obj_list:
        if user_obj.is_valid_password(password):
            # create a new session since no session exists
            from api.v1.app import auth
            session_id = auth.create_session(user_obj.id)
            response = jsonify(user_obj.to_json())
            response.set_cookie(getenv('SESSION_NAME'), session_id)
            return response
        else:
            return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    Handle a DELETE request to '/auth_session/logout'.

    Returns:
        str: An empty JSON response.

    Raises:
        404: If the session cannot be destroyed.

    Example Usage:
        DELETE /api/v1/auth_session/logout
    """
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
