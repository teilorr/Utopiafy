from __future__ import annotations
import typing as t

from utils.databases import AfkDB
from discord.ext import commands
import discord
import re

if t.TYPE_CHECKING:
    from core import Utopify

class Afk(commands.Cog):
    def __init__(self, bot: Utopify) -> None:
        self.bot = bot
        self.hidden = True

        self.afks: dict[int, str] = {}
        self.bot.loop.create_task(self.setup_cache())
        self.mention_regex = re.compile(r"(<@(|!|)\d*>)")

    async def setup_cache(self):
        async with AfkDB() as db:
            async with db.conn.cursor() as cursor:
                await cursor.execute(f"SELECT * FROM {db.table_name}")
                rows = await cursor.fetchall()
                if not rows:
                    return

                for column in rows:
                    self.afks[column[0]] = column[1]

    async def remove_afk(self, user_id: int) -> None:
        async with AfkDB() as db:
            await db.remove(user_id)
            self.afks.pop(user_id)

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message) -> None:
        mention_results: list[str] = self.mention_regex.findall(message.content)
        mentions = [x[0].replace('!', '') for x in mention_results]

        if message.author.id not in self.afks:
            async with AfkDB() as db:
                r = await db.select_user(message.author.id)
                if not r:
                    return

                self.afks[r[0]] = r[1]

        for user, reason in self.afks.items():
            m = f"<@{user}>"
            u = message.guild.get_member(user)
            if m in mentions and u:
                await message.channel.send(f"> {u.name.capitalize()} está afk: {reason}")

        if message.author.id in self.afks:
            await self.remove_afk(message.author.id)
            await message.channel.send(f"> Bem vindo de volta, *{message.author.name}*! Removi seu afk", delete_after=10)
            
            return 

async def setup(bot: Utopify) -> None:
    cog = Afk(bot)
    await bot.add_cog(cog)