from passlib.context import CryptContext

hashing = CryptContext(schemes=["argon2"], deprecated="auto")


def hash(password : str):
    return hashing.hash(password)


def password_verify(password : str, password_hash : str):
    return hashing.verify(password, password_hash)