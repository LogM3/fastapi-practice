from fastapi import HTTPException


class UserNotFoundError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail='User not found')


class UsernameExistsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail='Username exists')


class WrongCredentialsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail='Wrong Credentials')
