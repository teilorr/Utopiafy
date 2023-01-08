from __future__ import annotations
from typing import (
    TYPE_CHECKING
)

from discord.ext import commands
from utils import Cog
import discord

from utils.others.markovchat import MarkovModel
from utils.databases.markovdb import ChatDBManager

if TYPE_CHECKING:
    from core import Utopify
    from sqlite3 import Cursor

class MarkovChat(Cog, hidden=True):
    def __init__(self, bot: Utopify) -> None:
        self.bot = bot
        self.cooldown = 0

    async def generate_message(self, cur: Cursor, last_msg: str, db: ChatDBManager) -> str:
        text, total, _ = await db.get_full_text(cur)
        markov_model = MarkovModel(text)
        chain = markov_model.create_markov_chain(markov_model.get_tokens(), 1)
        msg_len = len(last_msg.split())
        if total > 15:
            if msg_len <= 20:
                msg = markov_model.generate_text(chain, msg_len * 2)
            else:
                msg = markov_model.generate_text(chain, 20)
            
            return msg.lower() if msg.lower().startswith("h") else msg.lower().capitalize()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.is_system():
            return

        if message.guild is None:
            return

        if message.clean_content.startswith("=="): 
            return

        if message.channel.id != 794453931412684820:
            return

        db = ChatDBManager()
        conn, cur = await db.create_connection(message.guild.id)

        content = message.content.replace(f"<@{self.bot.user.id}>", "")

        if message.content.lower() != ("k" * len(content)):
            await db.add_message_to_db(conn, cur, content.capitalize())
        self.cooldown += 1

        if message.content.startswith(f"<@{self.bot.user.id}>") or self.cooldown >= 52:
            if self.cooldown >= 52:
                self.cooldown = 0

            async with message.channel.typing():
                msg = await self.generate_message(cur, message.content, db)
                await message.reply(
                    content=msg, 
                    allowed_mentions=discord.AllowedMentions(
                        users=False, 
                        everyone=False, 
                        roles=False
                    )
                )
        await db.close_connection(conn, cur)

async def setup(bot: Utopify) -> None:
    cog = MarkovChat(bot)
    await bot.add_cog(cog)