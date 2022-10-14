from __future__ import annotations
import asyncio
from typing import (
    TYPE_CHECKING
)

from discord.ext import commands
import discord

from utils.databases import LevesDatabase
from random import Random

if TYPE_CHECKING:
    from core import Utopify

random = Random()


# FASE DE TESTES!
class Levels(commands.Cog):
    def __init__(self, bot: Utopify) -> None:
        self.bot = bot
        self.on_cooldown: set[discord.Member] = set()

    @commands.Cog.listener("on_message")
    async def add_xp(self, message: discord.Message) -> None:
        ignored_channels = [983499464893403167, 983499464893403167, 794455198188961823, 794454329167446076, 985340942087229470]
        if message.channel.id in ignored_channels:
            return

        if message.author.bot:
            return

        if message.author in self.on_cooldown:
            return

        xp = random.randint(15, 25)
        async with LevesDatabase() as db:
            total_xp, lvl = await db.increment_xp(message.author.id, xp)
            if total_xp and lvl:
                await message.channel.send(f"> Parabéns *{message.author.name}*, você acabou de upar pro ***level {lvl}*** com ***{total_xp}xp***!")
            
        self.on_cooldown.add(message.author)
        await asyncio.sleep(60)
        self.on_cooldown.remove(message.author)


async def setup(bot: Utopify) -> None:
    cog = Levels(bot)
    await bot.add_cog(cog)