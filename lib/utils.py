#!/usr/bin/env python
from cryptography.fernet import Fernet


def generate_key() -> None:
    """
    Generates a key and save it into a file
    """

    key = Fernet.generate_key()

    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    # end with
# end def


def load_key() -> bytes:
    """
    Loads the key named `secret.key` from the current directory
    """
    return open("secret.key", "rb").read()
# end def


def encrypt_password(password: str) -> str:
    """
    Returns an encrypted password
    """
    encoded_password = password.encode()

    f = Fernet(load_key())

    return f.encrypt(encoded_password).decode()
# end def


def decrypt_password(hashed_password: str) -> str:
    """
    Returns a decrypted password
    """

    f = Fernet(load_key())

    return f.decrypt(hashed_password.encode()).decode()
# end def
