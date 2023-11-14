#!/usr/bin/env python3
""" Inegration test"""

import requests

url = 'http://localhost:5000'
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

# use data in the request argument becos we are sending it as a form


def register_user(email: str, password: str) -> None:
    """ Validate user registration """
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post('{}/users'.format(url), data=payload)
    msg = {"email": email, "message": "user created"}
    assert response.status_code == 200
    assert response.json() == msg
    # try to register same user again to check if it raises an error
    # response = requests.post('{}/users'.format(url), data=payload)
    # assert response.status_code == 400
    # assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Validate log in with wrong password data """
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post('{}/sessions'.format(url), data=payload)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Valdate succesful log in with correct credentials """
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post('{}/sessions'.format(url), data=payload)
    msg = {"email": email, "message": "logged in"}
    assert response.status_code == 200
    assert response.json() == msg
    session_id = response.cookies.get("session_id")
    return session_id


def profile_unlogged() -> None:
    """ Validate user profile request request without log in """
    cookies = {
        "session_id": ""
    }
    response = requests.get('{}/profile'.format(url), cookies=cookies)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Validate profile request while logged in """
    cookies = {
        "session_id": session_id
    }
    response = requests.get('{}/profile'.format(url), cookies=cookies)
    msg = {"email": EMAIL}
    assert response.status_code == 200
    assert response.json() == msg


def log_out(session_id: str) -> None:
    """ Validate log out endpoint """
    cookies = {
        "session_id": session_id
    }
    response = requests.delete('{}/sessions'.format(url), cookies=cookies)
    msg = {"message": "Bienvenue"}
    assert response.status_code == 200
    assert response.json() == msg


def reset_password_token(email: str) -> str:
    """ Validate password reset token """
    payload = {
        "email": email
    }
    response = requests.post(
        '{}/reset_password'.format(url), data=payload)
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    msg = {"email": email, "reset_token": reset_token}
    assert response.json() == msg
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Validate password reset (update) """
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put('{}/reset_password'.format(url), data=payload)
    msg = {"email": email, "message": "Password updated"}
    assert response.status_code == 200
    assert response.json() == msg
    # print(response.json())


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    # print(reset_token)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
