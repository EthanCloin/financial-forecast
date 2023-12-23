from passlib.hash import pbkdf2_sha256


def encrypt_password(plain_password: str) -> str:
    return pbkdf2_sha256.hash(plain_password)
