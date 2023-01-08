from __future__ import annotations
import typing as t

from discord.ext import commands

class Cog(commands.Cog):
    def __init_subclass__(cls, **kwargs: t.Any) -> None:
        cls._hidden = kwargs.get("hidden", False)

    def is_hidden(self) -> bool:
        return self._hidden