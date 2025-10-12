from fastapi import APIRouter
from app.request_test.schema import TestJson
from app.request_test.service import RequestService


router: APIRouter = APIRouter(prefix='/test')


@router.get('/test/samplejson')
async def sample_json() -> list[TestJson]:
    service: RequestService = RequestService()
    return await service.get()
