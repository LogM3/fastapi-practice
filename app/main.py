from typing import Any
from fastapi import FastAPI, HTTPException, Request

from app.core.exceptions import TokenExpiredError
from app.users.handlers import router as user_router
from app.auth.handlers import router as auth_router
from app.auth.service import AuthService


app: FastAPI = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)


@app.middleware('http')
async def decode_token(request: Request, call_next):
    auth: str | None = request.headers.get('Authorization')
    if auth:
        splitted_auth: list[str] = auth.split()
        if len(splitted_auth) == 2 and splitted_auth[0].lower() == 'bearer':
            try:
                payload: dict[str, Any] = await AuthService.decode_token(
                    splitted_auth[1],
                    'access'
                )
            except TokenExpiredError as e:
                request.state.user_payload = e
            except HTTPException:
                pass
            else:
                request.state.user_payload = payload
    return await call_next(request)
