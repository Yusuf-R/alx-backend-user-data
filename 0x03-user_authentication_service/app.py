#!/usr/bin/env python3

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    Returns a JSON response with a message
    "Bienvenue" and a status code of 200.

    :return: JSON response
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """
    Register a user.

    Retrieves the email and password from the request form and checks if they are provided. # noqa E501
    Then checks if the email is already registered in the database. 
    If the email is not provided or the password is not provided, it returns an error response.  # noqa E501
    If the email is already registered, it returns an error response. 
    Otherwise, it registers the user and returns a success response with the user's email. # noqa E501

    Args:
        None

    Returns:
        A JSON response with the registered user's email and a success message
        if the user is registered successfully.
        A JSON response with an error message if the email or password is
        not provided or if the email is already registered.

    Example Usage:
        POST /users
        {
          "email": "example@example.com",
          "password": "password123"
        }
    """
    email = request.form.get('email')
    password = request.form.get('password')
    # verify email and password was passed
    if email is None:
        return jsonify({"message": "email is required"}), 400
    if password is None:
        return jsonify({"message": "password is required"}), 400
    # check if email credential already exists in the database
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Login a user and store their session.

    Retrieves the email and password from the request form, 
    verifies their presence, and then checks if the email and password combination is valid. # noqa: E501
    If the login is successful, it generates a session ID, stores it in a cookie, # noqa: E501
    and returns a JSON response with the user's email and a success message.

    Args:
        None

    Returns:
        A JSON response with the user's email and a success message.

    Raises:
        400 error: If the email or password is missing.
        401 error: If the email and password combination is invalid.

    Example Usage:
        POST /sessions
        {
          "email": "user@example.com",
          "password": "password123"
        }
    """
    email = request.form.get('email')
    password = request.form.get('password')
    # verify email and password was passed
    if email is None:
        abort(400, 'email is required')
    if password is None:
        abort(400, 'password is required')
    # verify email in database
    try:
        verify_user = AUTH.valid_login(email, password)
        if not verify_user:
            abort(401, 'invalid user')
        # generate session_id
        user = AUTH._db.find_user_by(email=email)
        session_id = AUTH.create_session(email)
        response = jsonify({"email": user.email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    except ValueError:
        abort(401, 'invalid user')


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logout a user by destroying their session.

    :return: None
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    Retrieves the user profile.

    This function handles a GET request to the '/profile' route.
    It retrieves the session ID from the request cookies and checks if it is not None. # noqa: E501

    If the session ID is None, it aborts the request with a 403 error.
    Otherwise, it calls the 'get_user_from_session_id' function from the 'AUTH' object # noqa: E501
    to retrieve the user associated with the session ID.

    If the user is None, it aborts the request with a 403 error. 
    Finally, it returns a JSON response containing the user's email with a 200 status code. # noqa: E501

    :return: A JSON response containing the user's email with a 200 status code. # noqa: E501
             - 200 status code: The request was successful
             - 403 status code: The request was not successful             
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    Retrieves the email from the request form data and generates
    a reset token for password reset.

    Returns:
        200 status code: A JSON response containing the user's email
        and the reset token.

    Raises:
        400 error: If the email is not provided.
        403 error: If there is an error finding the user or generating the
        reset token.
    """
    email = request.form.get('email')
    if email is None:
        abort(403, 'email is required')
    try:
        user = AUTH._db.find_user_by(email=email)
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": user.email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    Update the password for a user.

    This function is called when the Flask route '/reset_password' is accessed
    with a PUT request.
    It retrieves the email, reset token, and new password from the request form. # noqa: E501
    If any of these values are missing, a 400 error is returned. 
    Otherwise, it finds the user associated with the email,
    updates their password using the reset token, and returns a JSON response
    with the user's email and a success message.

    :return:  JSON response with the user's email and a success message.
             - 200  if the password was updated successfully
             - 400  if any of the required fields are missing
             - 403  if the user is not found or if the reset token is invalid
    """
    email = request.form.get('email')
    if email is None:
        abort(400, 'email is required')
    reset_token = request.form.get('reset_token')
    if reset_token is None:
        abort(400, 'reset_token is required')
    new_password = request.form.get('new_password')
    if new_password is None:
        abort(400, 'new_password is required')
    try:
        user = AUTH._db.find_user_by(email=email)
        if user is None:
            abort(403, 'user not found')
        if reset_token != user.reset_token:
            abort(403, 'invalid reset token')
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200  # noqa E501
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
