from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class PasswordCrypter:

    @staticmethod
    def get_hash(password: str):
        return context.hash(password)

    @staticmethod
    def verify(plain_password, hashed_password):
        return context.verify(plain_password, hashed_password)