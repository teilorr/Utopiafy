from __future__ import annotations
from typing import (
    Optional,
    Any 
)

from dataclasses import dataclass
from .base import Database
from uuid import uuid1
import datetime as dt
import discord
import asqlite

@dataclass
class Warn:
    user_id: int
    guild_id: int
    warn_id: int
    author_id: int
    reason: str
    warned_at: dt.datetime

    @classmethod
    def from_dict(cls, dict: dict[str, Any]) -> Warn:
        return cls(
            user_id=dict.get("user_id"),
            guild_id=dict.get("guild_id"),
            warn_id=dict.get("warn_id"),
            author_id=dict.get("author_id"),
            reason=dict.get("reason"),
            warned_at=dict.get("warned_at")
        )

    @classmethod
    def from_sqlite_row(cls, row: asqlite.sqlite3.Row) -> Warn:
        if not isinstance(row, asqlite.sqlite3.Row):
            raise TypeError(f"row Must be a sqlite3.Row instance, not {row.__class__.__name__!r}")

        return cls(
            user_id=row[0],
            guild_id=row[1],
            author_id=row[2],
            reason=row[3],
            warn_id=row[4],
            warned_at=dt.datetime.fromtimestamp(row[5])
        )

class WarningsDatabase(Database):
    def __init__(self) -> None:
        super().__init__("./data/warns.db")

    async def on_ready(self) -> None:
        await self.create_table(
            "warns", 
            table_attrs=(
                "user_id INTEGER", 
                "guild_id INTEGER", 
                "author_id INTEGER", 
                "reason TEXT", 
                "warn_id INTEGER", 
                "warned_at INTEGER"
                )
            )

    async def warn(self, member: discord.Member, /, reason: str, warn_author: discord.Member) -> Warn:
        data = await self._insert(
            user_id=member.id,
            guild_id=member.guild.id,
            author_id=warn_author.id,
            reason=reason, 
            warn_id=hash(str(uuid1())) % 100000000,
            warned_at=dt.datetime.now().timestamp()
        )
        return Warn.from_dict(dict=dict(data))

    async def get_warns_from(self, member: discord.Member) -> Optional[list[Warn]]:
        warns: list[Warn] = []
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE user_id=? AND guild_id=?",
                (member.id, member.guild.id)
            )
            
            rows = await cursor.fetchall()
            if not rows:
                return None

            for row in rows:
                warns.append(Warn.from_sqlite_row(row))
        return warns

    async def clear_warns_from(self, member: discord.Member, /, current_guild: discord.Guild) -> list[Warn]:
        warns: list[Warn] = []
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE user_id=? AND guild_id=?",
                (member.id, current_guild.id)
            )
            for row in await cursor.fetchall():
                warns.append(Warn.from_sqlite_row(row))

            await cursor.execute(
                f"DELETE FROM {self.table_name} WHERE user_id=? AND guild_id=?", 
                (member.id, current_guild.id)
            )
        return warns

    async def delete_warn(self, /, warn_id: int, current_guild: discord.Guild) -> Optional[Warn]:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE warn_id=? AND guild_id=?",
                (warn_id, current_guild.id)
            )
            
            if not (row := await cursor.fetchone()):
                return None
 
            warn = Warn.from_sqlite_row(row)
            await cursor.execute(
                f"DELETE FROM warns WHERE warn_id=? AND guild_id=?",
                (warn_id, current_guild.id)
            )

            return warn

    async def user_has_warns(self, user_id: int, /, *, current_guild: discord.Guild) -> bool:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                f"SELECT user_id FROM {self.table_name} WHERE user_id=? AND guild_id=?", 
                (user_id, current_guild.id)
            )
            return bool(await cursor.fetchone())
