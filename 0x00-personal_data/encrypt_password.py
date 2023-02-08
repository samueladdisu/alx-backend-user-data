#!/usr/bin/env python3

"""
bcrypt for password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ hash_password """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check if password is valid"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
