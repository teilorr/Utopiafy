from __future__ import annotations
from typing import (
    TYPE_CHECKING
)

from utils import WarningsDatabase
from discord.ext import commands
from discord import app_commands
import discord

if TYPE_CHECKING:
    from core import Utopify

class AppMenuCog(commands.Cog):
    def __init__(self, bot: Utopify) -> None:
        self.bot = bot
        self.ctx_menu_user_info = app_commands.ContextMenu(
           name="Ver Informações",
           callback=self.ctx_menu_userinfo_callback
        )

        self.hidden = True

    async def ctx_menu_userinfo_callback(self, interaction: discord.Interaction, member: discord.Member) -> None:
            joined_at_formated = discord.utils.format_dt(member.joined_at)
            created_at_formated = discord.utils.format_dt(member.created_at)
            joined_at_formated_relative = discord.utils.format_dt(member.joined_at, "R")
            created_at_formated_relative = discord.utils.format_dt(member.created_at, "R")

            async with WarningsDatabase() as db:
                embed = discord.Embed(
                    title=f"Informações sobre {member}",
                    color=discord.Color.blurple()
                )
                embed.add_field(name=f"\U0001f530 `Apelido`", value=f"***{member.nick or 'Nenhum'}***" , inline=True)
                embed.add_field(name=f"\U0001f4e1 `ID`", value=f"***{member.id}***" , inline=True)
                embed.add_field(name=f"\U0001f4c5 `Criação da conta`", value=f"{created_at_formated} / {created_at_formated_relative}", inline=False)
                embed.add_field(name=f"\U00002728 `Entrou no servidor`", value=f"{joined_at_formated} / {joined_at_formated_relative}", inline=False)
                embed.add_field(name=f"\U0001f4f8 `Maior cargo`", value=f"{member.top_role.mention}")
                embed.add_field(name=f"\U0001f4e2 `Quantidade de warns`", value=f"{len(await db.get_warns_from(member) or '')} Avisos", inline=False)
                embed.set_thumbnail(url=member.display_avatar.url)

                await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: Utopify):
    cog = AppMenuCog(bot)
    for attr, value in cog.__dict__.items():
        if not (attr.startswith("__") and attr.endswith("__")) \
                and attr.startswith("ctx_menu"):
            bot.tree.add_command(value)

    await bot.add_cog(cog)