from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


class PasswordService:
    pwd_context: CryptContext = CryptContext(schemes=['bcrypt'])

    @classmethod
    async def get_pwd_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    async def verify_pwd_hash(cls, hashed: str, password: str) -> bool:
        return cls.pwd_context.verify(password, hashed)


pwd_service: PasswordService = PasswordService()
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer('/auth/login')
