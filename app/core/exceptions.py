from fastapi import HTTPException


class UserNotFoundError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail='User not found')


class UsernameExistsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail='Username exists')


class WrongCredentialsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail='Wrong Credentials')


class TokenExpiredError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail='Token expired')


class InvalidTokenError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail='Token invalid')


class WrongTokenTypeError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail='Wrong token type')


class ProjectNotFoundError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail='Project not found')


class WrongDataError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail='Wrong Project Data')
