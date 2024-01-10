from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


class Hash():
    def bcrypt(password: str):
        return pwd_context.hash(password)

    def verify(hashed_pwd, pwd):
        return pwd_context.verify(pwd, hashed_pwd)
