import re

import bcrypt


def check_email_valid(email) -> bool:
    return (
        re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)
        is not None
    )


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password: bytes, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password, hashed_password)
