from __future__ import annotations
from typing import (
    Optional,
    Union,
    Any
)

from dataclasses import dataclass
from .base import Database

@dataclass
class Suggestion:
    id: str
    message_id: int 
    user_id: int

    @classmethod
    def from_dict(cls, dict: dict[str, Any]) -> Suggestion:
        return cls(
            id=dict.get("id"),
            message_id=dict.get("message_id"),
            user_id=dict.get("user_id")
        )

class Suggestions(Database):
    def __init__(self) -> None:
        super().__init__("./data/suggestions.db")

    async def on_ready(self) -> None:
        await self.create_table(
            "suggestions", 
            table_attrs=(
                "id VARCHAR(12)",
                "message_id INTEGER(20)",
                "user_id INTEGER(20)", 
                )
            )

    async def create(self, suggestion_id: int, message_id: int, user_id: int) -> Suggestion:
        data = await self._insert(
            id=suggestion_id,
            message_id=message_id,
            user_id=user_id
        )
        return Suggestion.from_dict(data)

    async def _delete_where(self, id) -> Optional[Union[list[Suggestion], Suggestion]]:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "SELECT * FROM {0} WHERE id=?".format(self.table_name), id
            )
            row = await cursor.fetchone()
            if not row:
                return None

            suggestion = Suggestion(
                id=row[0],
                message_id=row[1],
                user_id=row[2]
            )

            await cursor.execute(
                "DELETE FROM {0} WHERE id=?".format(self.table_name), id
            )
        return suggestion

    async def reject(self, s_id: str) -> Suggestion:
        return await self._delete_where(id=s_id)

    async def approve(self, s_id: str) -> Suggestion:
        return await self._delete_where(id=s_id)