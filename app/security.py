from passlib.hash import pbkdf2_sha256


def encrypt_password(plain_password: str) -> str:
    return pbkdf2_sha256.hash(plain_password)


def verify_password(provided: str, stored_hash: str) -> bool:
    return pbkdf2_sha256.verify(provided, stored_hash)
