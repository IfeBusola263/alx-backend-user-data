#!/usr/bin/env python3
"""
This module test the end points for the correct payload and status code.
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    This method tests the endpoint for user registeration.
    """
    # credentials sent
    payload = {'email': email, 'password': password}

    # send the request
    response = requests.post('http://localhost:5000/users', data=payload)
    expected_payload = {
        "email": email,
        "message": "user created",
    }

    # validate response
    assert response.status_code == 200
    assert response.json() == expected_payload


def log_in_wrong_password(email: str, password: str) -> None:
    """
    This function tests for the users endpoint, with the
    wrong credentials.
    """
    # credentials sent
    payload = {'email': email, 'password': password}

    # send the request
    response = requests.post('http://localhost:5000/sessions', data=payload)

    # validate response
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    This method returns the session_id of the request to login.
    """
    # credentials sent
    payload = {'email': email, 'password': password}

    # send the request
    response = requests.post('http://localhost:5000/sessions', data=payload)
    session_id = response.cookies.get('session_id')
    expected_payload = {"email": email, "message": "logged in"}

    assert response.status_code == 200
    assert response.json() == expected_payload
    return session_id


def profile_unlogged() -> None:
    """
    This function tests for profile status code,
    when profile is not logged in.
    """
    response = requests.get('http://localhost:5000/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    This function tests for a successfully logged in user and
    request to view profile.
    """
    payload = {'session_id': session_id}
    response = requests.get('http://localhost:5000/profile', cookies=payload)
    expected_payload = {"email": "guillaume@holberton.io"}
    print(response.json())

    assert response.status_code == 200
    assert response.json() == expected_payload


def log_out(session_id: str) -> None:
    """
    This function tests for the successful logout of the
    user.
    """
    payload = {'session_id': session_id}
    response = requests.delete(
        'http://localhost:5000/sessions', cookies=payload)

    assert response.status_code == 301


def reset_password_token(email: str) -> str:
    """
    This fucntion tests for the password reset_token generated
    by the user and returns the reset_token.
    """

    payload = {'email': email}
    response = requests.post(
        'http://localhost:5000/reset_password', data=payload)

    res = response.json()
    token = res.get('reset_token')
    expected_payload = {"email": email, "reset_token": token}

    assert response.status_code == 200
    assert res == espected_payload
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    This method tests if the user password
    update endpoint resolves. Returns Nothing
    """

    payload = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }

    response = requests.put(
        'http://localhost:5000/reset_password', data=payload)
    res = response.json()
    expected_payload = {'email': email, "message": "Password updated"}

    assert response.status_code == 200
    assert response.json() == expected_payload


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
