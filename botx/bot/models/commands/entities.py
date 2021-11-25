from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from botx.bot.models.commands.enums import MentionTypes
from botx.shared_models.chat_types import ChatTypes


@dataclass
class Mention:
    type: MentionTypes
    entity_id: Optional[UUID] = None
    name: Optional[str] = None

    def __str__(self) -> str:
        name = self.name or ""
        entity_id = self.entity_id or ""
        mention_type = self.type.value
        return f"<embed_mention>{mention_type}:{entity_id}:{name}</embed_mention>"

    @classmethod
    def user(cls, huid: UUID, name: Optional[str] = None) -> "Mention":
        return cls(
            type=MentionTypes.USER,
            entity_id=huid,
            name=name,
        )

    @classmethod
    def contact(cls, huid: UUID, name: Optional[str] = None) -> "Mention":
        return cls(
            type=MentionTypes.CONTACT,
            entity_id=huid,
            name=name,
        )

    @classmethod
    def chat(cls, chat_id: UUID, name: Optional[str] = None) -> "Mention":
        return cls(
            type=MentionTypes.CHAT,
            entity_id=chat_id,
            name=name,
        )

    @classmethod
    def channel(cls, chat_id: UUID, name: Optional[str] = None) -> "Mention":
        return cls(
            type=MentionTypes.CHANNEL,
            entity_id=chat_id,
            name=name,
        )

    @classmethod
    def all(cls) -> "Mention":
        return cls(type=MentionTypes.ALL)


@dataclass
class Forward:
    chat_id: UUID
    huid: UUID
    type: ChatTypes
    chat_name: str
    sync_id: UUID
    created_at: datetime


@dataclass
class Reply:
    chat_id: UUID
    huid: UUID
    type: ChatTypes
    chat_name: str
    sync_id: UUID
    body: str


Entity = Union[Mention, Forward, Reply]
