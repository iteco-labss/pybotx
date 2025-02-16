from typing import Optional
from uuid import UUID

import pytest

from pybotx import (
    Bot,
    BotAccount,
    BotAccountWithSecret,
    CTSLogoutEvent,
    HandlerCollector,
    lifespan_wrapper,
)

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.mock_authorization,
    pytest.mark.usefixtures("respx_mock"),
]


async def test__cts_logout__succeed(
    bot_account: BotAccountWithSecret,
) -> None:
    # - Arrange -
    payload = {
        "bot_id": "24348246-6791-4ac0-9d86-b948cd6a0e46",
        "command": {
            "body": "system:cts_logout",
            "data": {
                "user_huid": "b9197d3a-d855-5d34-ba8a-eff3a975ab20",
                "cts_id": "8dada2c8-67a6-4434-9dec-570d244e78ee",
            },
            "command_type": "system",
            "metadata": {},
        },
        "source_sync_id": None,
        "sync_id": "2c1a31d6-f47f-5f54-aee2-d0c526bb1d54",
        "from": {
            "ad_domain": None,
            "ad_login": None,
            "app_version": None,
            "chat_type": None,
            "device": None,
            "device_meta": {
                "permissions": None,
                "pushes": None,
                "timezone": None,
            },
            "device_software": None,
            "group_chat_id": None,
            "host": "cts.example.com",
            "is_admin": None,
            "is_creator": None,
            "locale": "en",
            "manufacturer": None,
            "platform": None,
            "platform_package_id": None,
            "user_huid": None,
            "username": None,
        },
        "proto_version": 4,
    }

    collector = HandlerCollector()
    cts_logout: Optional[CTSLogoutEvent] = None

    @collector.cts_logout
    async def cts_logout_handler(event: CTSLogoutEvent, bot: Bot) -> None:
        nonlocal cts_logout
        cts_logout = event
        # Drop `raw_command` from asserting
        cts_logout.raw_command = None

    built_bot = Bot(collectors=[collector], bot_accounts=[bot_account])

    # - Act -
    async with lifespan_wrapper(built_bot) as bot:
        bot.async_execute_raw_bot_command(payload)

    # - Assert -
    assert cts_logout == CTSLogoutEvent(
        bot=BotAccount(
            id=UUID("24348246-6791-4ac0-9d86-b948cd6a0e46"),
            host="cts.example.com",
        ),
        raw_command=None,
        huid=UUID("b9197d3a-d855-5d34-ba8a-eff3a975ab20"),
    )
