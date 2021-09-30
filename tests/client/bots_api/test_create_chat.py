from http import HTTPStatus
from uuid import UUID

import httpx
import pytest
import respx

from botx import Bot, BotAccount, HandlerCollector, lifespan_wrapper
from botx.bot.bot_accounts_storage import BotAccountsStorage
from botx.bot.models.commands.enums import ChatTypes


@pytest.fixture
def chat_id() -> UUID:
    return UUID("b46b18ee-88e8-452f-864a-993df921321e")


@respx.mock
@pytest.mark.asyncio
async def test_create_chat(
    httpx_client: httpx.AsyncClient,
    host: str,
    bot_id: UUID,
    bot_signature: str,
    bot_account: BotAccount,
    prepared_bot_accounts_storage: BotAccountsStorage,
    chat_id: UUID,
    mock_authorization: None,
) -> None:
    # - Arrange -
    endpoint = respx.post(
        f"https://{host}/api/v3/botx/chats/create",
        headers={"Authorization": "Bearer token", "Content-Type": "application/json"},
    ).mock(
        return_value=httpx.Response(
            HTTPStatus.OK,
            json={
                "status": "ok",
                "result": {"chat_id": str(chat_id)},
            },
        ),
    )

    built_bot = Bot(
        collectors=[HandlerCollector()],
        bot_accounts=[bot_account],
        httpx_client=httpx_client,
    )

    # - Act -
    async with lifespan_wrapper(built_bot) as bot:
        created_chat_id = await bot.create_chat(
            bot_id,
            "TEST_CHAT_NAME",
            ChatTypes.GROUP_CHAT,
            [],
        )

    # - Assert -
    assert created_chat_id == chat_id
    assert endpoint.called
