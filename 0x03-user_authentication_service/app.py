#!/usr/bin/env python3

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ Index page"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """ Register user"""
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
    """ login a user and store it's session"""
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
    """ logout a user"""
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
    """ get user profile"""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ get reset token"""
    email = request.form.get('email')
    if email is None:
        abort(400, 'email is required')
    try:
        user = AUTH._db.find_user_by(email=email)
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": user.email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ update password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    if email is None or reset_token is None or new_password is None:
        abort(400, 'email, reset_token and new_password are required')
    try:
        user = AUTH._db.find_user_by(email=email)
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": user.email, "message": "Password updated"}), 200  # noqa
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
