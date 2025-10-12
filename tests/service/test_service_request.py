from respx import mock
from httpx import Response
from pytest import mark

from app.request_test.service import RequestService


@mark.service
async def test_request_service_get_success():
    data = [
        {"userId": 1, "id": 1, "title": "t1", "body": "b1"},
        {"userId": 2, "id": 2, "title": "t2", "body": "b2"},
    ]

    async with mock as m:
        route = m.get(RequestService.url).mock(
            return_value=Response(200, json=data))
        result = await RequestService().get()
        assert route.called
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].id == 1
        assert result[0].title == "t1"
