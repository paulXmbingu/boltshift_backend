"""
# This file if for handling the relevant security patches of the project:
- Hashing registration passwords
"""
import hashlib

def hash_password(pass1, pass2):
    try:
        if pass1 == pass2:
            # generating password bytes by encoding
            pass_bytes = pass1.encode("utf-8")
            # hashing the bytes
            hashed_pass = hashlib.sha256(pass_bytes).hexdigest()
            return hashed_pass
        else:
            return SystemError
    except Exception as error:
        return error