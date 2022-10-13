import asqlite
import os

from typing_extensions import Self
from typing import (
    TypeVar
)
from .errors import (
    BadArgument, 
)

T_DICT = TypeVar("T_DICT", bound=dict)

class Database:
    def __init__(self, fp: str) -> None:
        if not os.path.splitext(fp)[1] == ".db":
            raise BadArgument(
                f"fp must be a SQLite .db file, not {os.path.splitext(fp)[1]}"
            )
        fp = fp.replace("\\", "/")
        self.fp: str = fp
        self.table_name: str | None = None
        
        if not os.path.isfile(self.fp):
            with open(self.fp, "x"): ...

    async def __aenter__(self) -> Self:
        self.conn = await asqlite.connect(self.fp)
        await self.on_ready()

        return self

    async def __aexit__(self, *args, **kwargs):
        return await self.conn.__aexit__(*args, **kwargs)

    async def _execute(self, query: str, *args) -> None:
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, *args)
            await self.conn.commit()

    async def _insert(self, **kwargs: T_DICT) -> T_DICT:
        args = kwargs.values()

        # no idea how this works, it just manipulates the query in a way that i don't know how i made it
        await self._execute(
            f"INSERT INTO {self.table_name}({', '.join(kwargs.keys())}) VALUES({('?, '*len(args)).strip(', ')})",
            tuple(args)
        )
        return kwargs

    async def create_table(self, table_name: str, /, table_attrs: tuple) -> None:
        self.table_name = table_name
        await self._execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(table_attrs)})"
        )

    async def on_ready(self) -> None:
        ...