from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta, timezone


def encrypt_password(plain_password: str) -> str:
    return pbkdf2_sha256.hash(plain_password)


def verify_password(provided: str, stored_hash: str) -> bool:
    return pbkdf2_sha256.verify(provided, stored_hash)


def is_session_expired(session: dict):
    now = datetime.now(timezone.utc)
    expires = datetime.fromisoformat(session.get("expires"))
    res = expires < now
    return res


def add_new_session_times(session: dict):
    created = datetime.now(timezone.utc)
    modified = created
    expires = created + timedelta(days=2)
    session.update(
        {
            "created": str(created.isoformat()),
            "modified": str(modified.isoformat()),
            "expires": str(expires.isoformat()),
        }
    )
    return session
