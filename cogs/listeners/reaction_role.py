from __future__ import annotations
from typing import (
    TYPE_CHECKING
)

from discord.ext import commands
from utils import Configs
from utils import Cog
import discord

if TYPE_CHECKING:
    from core import Utopify

class ReactionRole(Cog, hidden=True):
    def __init__(self, bot: Utopify):
        self.bot = bot
        self.reaction_message_id: int = Configs.reaction_role_message_id

    @commands.Cog.listener("on_raw_reaction_add")
    async def add_reaction_role(self, payload: discord.RawReactionActionEvent) -> None:
        if payload.user_id == self.bot.user.id:
            return

        guild = await self.bot.fetch_guild(payload.guild_id)
        user = await guild.fetch_member(payload.user_id)

        if payload.message_id == self.reaction_message_id:
            if str(payload.emoji) == '🧪':
                role = discord.utils.get(guild.roles, name='=Dorgas')
                await user.add_roles(role)

            elif str(payload.emoji) == '⏰':
                role = discord.utils.get(guild.roles, name='=Nostalgic')
                await user.add_roles(role)

            elif str(payload.emoji) == '✨':
                role = discord.utils.get(guild.roles, name="=Newsletter")
                await user.add_roles(role)

            elif str(payload.emoji) == '🌲':
                role = discord.utils.get(guild.roles, name="=Farlands")
                await user.add_roles(role)

            elif str(payload.emoji) == '🎮':
                role = discord.utils.get(guild.roles, name="=Players")
                await user.add_roles(role)

            elif str(payload.emoji) == '💰':
                role = discord.utils.get(guild.roles, name="=Capitalista")
                await user.add_roles(role)

            elif str(payload.emoji) == '🔔':
                role = discord.utils.get(guild.roles, name="=Sininho")
                await user.add_roles(role)

            elif str(payload.emoji) == '👾':
                role = discord.utils.get(guild.roles, name="=Speedrunner")
                await user.add_roles(role)

            elif str(payload.emoji) == '🎊':
                role = discord.utils.get(guild.roles, name="=Puddings 2022")
                await user.add_roles(role)

    @commands.Cog.listener("on_raw_reaction_remove")
    async def remove_reaction_role(self, payload: discord.RawReactionActionEvent) -> None:
        if payload.user_id == self.bot.user.id:
            return

        guild = await self.bot.fetch_guild(payload.guild_id)
        user = await guild.fetch_member(payload.user_id)

        if payload.message_id == self.reaction_message_id:
            if str(payload.emoji) == '🧪':
                role = discord.utils.get(guild.roles, name='=Dorgas')
                await user.remove_roles(role)

            elif str(payload.emoji) == '⏰':
                role = discord.utils.get(guild.roles, name='=Nostalgic')
                await user.remove_roles(role)

            elif str(payload.emoji) == '✨':
                role = discord.utils.get(guild.roles, name="=Newsletter")
                await user.remove_roles(role)

            elif str(payload.emoji) == '🌲':
                role = discord.utils.get(guild.roles, name="=Farlands")
                await user.remove_roles(role)

            elif str(payload.emoji) == '🎮':
                role = discord.utils.get(guild.roles, name="=Players")
                await user.remove_roles(role)

            elif str(payload.emoji) == '💰':
                role = discord.utils.get(guild.roles, name="=Capitalista")
                await user.remove_roles(role)

            elif str(payload.emoji) == '🔔':
                role = discord.utils.get(guild.roles, name="=Sininho")
                await user.remove_roles(role)

            elif str(payload.emoji) == '👾':
                role = discord.utils.get(guild.roles, name="=Speedrunner")
                await user.remove_roles(role)

            elif str(payload.emoji) == '🎊':
                role = discord.utils.get(guild.roles, name="=Puddings 2022")
                await user.remove_roles(role)

async def setup(bot: Utopify) -> None:
    cog = ReactionRole(bot)
    await bot.add_cog(cog)