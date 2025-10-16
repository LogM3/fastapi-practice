from typing import Annotated, Any
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db_connection
from app.core.exceptions import TokenExpiredError
from app.users.handlers import router as user_router
from app.auth.handlers import router as auth_router
from app.project.handlers import router as project_router
from app.request_test.handlers import router as test_router
from app.auth.service import AuthService


app: FastAPI = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(test_router)


@app.get('/')
async def root():
    return {'status': 'ok'}


@app.get('/db_check')
async def check_db(
    session: Annotated[AsyncSession, Depends(get_db_connection)]
) -> dict[str, str]:
    try:
        result = (
            await session.execute(text('SELECT version();'))).scalar_one()
        return {'version': result}
    except ConnectionRefusedError:
        raise HTTPException(500, 'Database unavailable')


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
