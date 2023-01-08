from __future__ import annotations
import typing as t

from discord.ext import commands
import discord

from utils.databases import WarningsDatabase
from utils import Cog

if t.TYPE_CHECKING:
    from core import Utopify

class Info(Cog):
    """:\U00002754:""" # Descrição para mostrar no ==help
    def __init__(self, bot: Utopify) -> None:
        self.bot = bot

    @commands.command(name="user_info", aliases=["userinfo"], help="Mostra informações de um usuário")
    async def user_info(self, ctx: commands.Context, member: t.Optional[discord.Member] = None) -> None:
        member = ctx.author if not member else member

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

        await ctx.send("Tente os comandos por context menu também!", embed=embed)

    @commands.command(name="ping", help="Mostra o ping do bot")
    async def _ping(self, ctx: commands.Context) -> None:
        await ctx.send(
            f"> `{self.bot.latency * 1000:.2f}ms` de latência \U0001f4e1"
        )

async def setup(bot: Utopify) -> None:
    cog = Info(bot)
    await bot.add_cog(cog)