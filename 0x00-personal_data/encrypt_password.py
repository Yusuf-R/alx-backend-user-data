#!/usr/bin/env python3
""" Implement Password Encryption using Bcrypt """

import bcrypt


def hash_password(password: str) -> bytes:
    """ Hash a password using Bcrypt """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
