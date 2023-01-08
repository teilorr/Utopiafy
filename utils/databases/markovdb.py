from __future__ import annotations
import typing as t

import os
import re
import asyncio
from sqlite3 import OperationalError

import asqlite

class ChatDBManager:
    def __init__(self, db_path: t.Optional[str] = "./data"):
        self.db_path = db_path

    async def create_connection(self, guild_id: int) -> tuple[asqlite.Connection, asqlite.Cursor]:
        exists_guild_db = os.path.isfile(f"{self.db_path}/{guild_id}.db")

        while True:
            try:
                conn = await asqlite.connect(f"{self.db_path}/{guild_id}.db")
                break
            except OperationalError:
                await asyncio.sleep(0)

        cur = await conn.cursor()

        if not exists_guild_db:
            await self.add_guild(conn, cur)

        return conn, cur

    async def close_connection(self, conn: asqlite.Connection, cur: asqlite.Cursor) -> None:
        await cur.close()
        await conn.close()

    async def add_guild(self, conn: asqlite.Connection, cur: asqlite.Cursor):
        await cur.execute("CREATE TABLE chatchannels (channel INT)")
        await cur.execute("CREATE TABLE trainchannels (channel INT)")
        await cur.execute(
            "CREATE TABLE messages (id INTEGER PRIMARY KEY, message TEXT)"
        )

        await conn.commit()

    def remove_guild(self, guild_id: int) -> None:
        os.remove(f"{self.db_path}/{guild_id}.db")

    async def add_chat_channel(self, conn: asqlite.Connection, cur: asqlite.Cursor, channel_id: int) -> t.Literal[1, 2, 3]:
        await cur.execute("SELECT channel FROM chatchannels")
        chat_channels = [row[0] async for row in cur]

        if channel_id in chat_channels:
            return 2

        if len(chat_channels) >= 5:
            return 3

        await cur.execute(
            "INSERT INTO chatchannels (channel) VALUES (?)", (channel_id,)
        )
        await conn.commit()
        return 1

    async def add_train_channel(self, conn: asqlite.Connection, cur: asqlite.Cursor, channel_id: int) -> t.Literal[1, 2, 3]:
        await cur.execute("SELECT channel FROM trainchannels")
        train_channels = [row[0] async for row in cur]

        if channel_id in train_channels:
            return 2

        if len(train_channels) >= 10:
            return 3

        await cur.execute(
            "INSERT INTO trainchannels (channel) VALUES (?)", (channel_id,)
        )
        await conn.commit()
        return 1

    async def is_chat_channel(self, cur: asqlite.Cursor, channel_id: int) -> bool:
        await cur.execute(
            "SELECT COUNT(channel) FROM chatchannels WHERE channel = ? LIMIT 1",
            (channel_id,),
        )

        check = await cur.fetchone()
        check = check[0]

        return check == 1

    async def is_train_channel(self, cur: asqlite.Cursor, channel_id: int) -> bool:
        await cur.execute(
            "SELECT COUNT(channel) FROM trainchannels WHERE channel = ? LIMIT 1",
            (channel_id,),
        )
        check = await cur.fetchone()
        check = check[0]

        return check == 1

    async def get_chat_channels(self, cur: asqlite.Cursor) -> list[int]:
        await cur.execute("SELECT channel FROM chatchannels")

        chat_channels = [row[0] async for row in cur]

        return chat_channels

    async def get_train_channels(self, cur: asqlite.Cursor) -> list[int]:
        await cur.execute("SELECT channel FROM trainchannels")

        train_channels = [row[0] async for row in cur]

        return train_channels

    async def reset_db(self, conn: asqlite.Connection, cur: asqlite.Cursor) -> None:
        for table in ["chatchannels", "trainchannels", "messages"]:
            await cur.execute(f"DROP TABLE {table}")

        await cur.execute("CREATE TABLE chatchannels (channel INT)")
        await cur.execute("CREATE TABLE learnchannels (channel INT)")
        await cur.execute(
            "CREATE TABLE messages (id INTEGER PRIMARY KEY, message TEXT)"
        )

        await conn.commit()

    async def add_message_to_db(self, conn: asqlite.Connection, cur: asqlite.Cursor, content: str) -> None:
        await cur.execute("INSERT INTO messages (message) VALUES (?)", (content,))

        await conn.commit()

    async def get_full_text(self, cur: asqlite.Cursor) -> tuple[str, str, str]:
        await cur.execute("SELECT message FROM messages")

        messages = await cur.fetchall()
        total = len(messages)
        text = " ".join([msg_tup[0] for msg_tup in messages])
        last_msg = messages[-1][0]

        return text, total, last_msg