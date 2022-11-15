from __future__ import annotations
from typing import (
    TYPE_CHECKING
)
from discord.ext import commands, tasks # type: ignore
import discord

if TYPE_CHECKING:
    from core import Utopify

class AutoGold(commands.Cog):
    def __init__(self, bot: Utopify) -> None:
        self.bot = bot
        self.hidden = True

    @commands.Cog.listener(name="on_ready")
    async def on_ready(self) -> None:
        self.add_roles.start()
        self.remove_roles.start()

    @tasks.loop(seconds=5)
    async def add_roles(self) -> None:
        roles_ids = [833796078544486405, 723652473855803425, 794461214012604437, 588752987590230037]
        for role_id in roles_ids:
            role = discord.utils.get(self.bot.utopia.roles, id=role_id) # type: ignore
            gold = discord.utils.get(self.bot.utopia.roles, id=794461214028988437) # type: ignore
            for member in role.members: # type: ignore
                if gold in member.roles:
                    continue

                await member.add_roles(gold) # type: ignore 

    @tasks.loop(seconds=10)
    async def remove_roles(self) -> None:
        gold = discord.utils.get(self.bot.utopia.roles, id=794461214028988437)
        role_list = (723652473855803425, 833796078544486405, 588752987590230037, 794461214012604437, 794460742128238602)
        
        for member in gold.members:
            for possible_role in role_list:
                pob_role = discord.utils.get(self.bot.utopia.roles, id=possible_role)
                no_roles = True

                if pob_role not in member.roles:
                    continue
                else:
                    no_roles = False
                    break

            if no_roles == True:
                await member.remove_roles(gold)
            else:
                continue

async def setup(bot: Utopify) -> None:
    cog = AutoGold(bot)
    await bot.add_cog(cog)