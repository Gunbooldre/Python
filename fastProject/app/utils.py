from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash(password: str) -> str:
    return pwd_context.hash(password)


def verify(plaint_password, hashed_password):
    return pwd_context.verify(plaint_password,hashed_password)