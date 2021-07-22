import uuid

import pytest

from botx import ChatTypes
from botx.clients.methods.v3.chats.create import Create
from botx.concurrency import callable_to_coroutine

pytestmark = pytest.mark.asyncio


async def test_chat_creation(client, requests_client):
    method = Create(
        host="example.com",
        name="test name",
        members=[uuid.uuid4()],
        chat_type=ChatTypes.group_chat,
        shared_history=False,
    )

    request = requests_client.build_request(method)
    await callable_to_coroutine(requests_client.execute, request)

    assert client.requests[0].name == method.name
    assert client.requests[0].members == method.members
