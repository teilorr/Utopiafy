from __future__ import annotations
import typing as t

from .base import Database

class AfkDB(Database):
    def __init__(self) -> None:
        super().__init__("./data/afk.db")

    async def on_ready(self) -> None:
        await self.create_table(
            "afk",
            table_attrs=(
                "user_id INTEGER UNIQUE NOT NULL",
                "reason VARCHAR NOT NULL"
            )
        )

    async def add(self, user_id: int, reason: str) -> None:
        await self._insert(
            user_id=user_id,
            reason=reason
        )

    async def remove(self, user_id: int) -> None:
        await self._execute(
            f"DELETE FROM {self.table_name} WHERE user_id=?",
            (user_id, )
        )

    async def select_user(self, user_id: int) -> None:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE user_id=?",
                (user_id)
            )
            return await cursor.fetchone()