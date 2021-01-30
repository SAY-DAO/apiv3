import os
from hashlib import sha256


def make_password(password):
    """
    v2 password hashing
        password: 64 bit hasshed + 64 bit salt
    """

    password = str(password)
    salt = sha256()
    salt.update(os.urandom(60))
    salt = salt.hexdigest()

    hashed_pass = sha256()
    # Make sure password is a str because we cannot hash unicode objects
    hashed_pass.update((password + salt).encode('utf-8'))
    hashed_pass = hashed_pass.hexdigest()

    password = salt + hashed_pass
    return password


def check_password(hashed_password, raw_password):
    """ v2 password checking """

    hashed_pass = sha256()
    hashed_pass.update((raw_password + hashed_password[:64]).encode('utf-8'))
    return hashed_password[64:] == hashed_pass.hexdigest()

