from __future__ import annotations
from typing import (
    TYPE_CHECKING
)

from discord.ext import commands
from utils import Configs
import discord

if TYPE_CHECKING:
    from core import Utopify

class ManageReports(commands.Cog):
    def __init__(self, bot: Utopify) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def change_embed_color(self, payload: discord.RawReactionActionEvent) -> None:
        if payload.user_id == self.bot.user.id:
            return

        report_channel = self.bot.get_channel(Configs.report_channel_id)
        
        if payload.channel_id == report_channel.id:
            msg = await report_channel.fetch_message(payload.message_id)
            if not msg.embeds:
                return 

            embed = msg.embeds[0]
            if str(payload.emoji) in ("\U00002705", "\U0001f7e9"): # quadrado verde
                embed.color = discord.Color.green()
            
            elif str(payload.emoji) == "\U0001f7e5": # quadrado vermelho
                embed.color = discord.Color.red()

            elif str(payload.emoji) == "\U0001f7e7": # quadrado laranja
                embed.color = discord.Color.orange()
             
            elif str(payload.emoji) == "\U00002b1c": # quadrado branco
                embed.color = 0xFFFFFF

            elif str(payload.emoji) == "\U0001f5d1": # lixeira
                await msg.delete()

            try:
                await msg.edit(embed=embed)
                await msg.clear_reactions()
            except (discord.NotFound, discord.HTTPException):
                pass

async def setup(bot: Utopify) -> None:
    cog = ManageReports(bot)
    await bot.add_cog(cog)