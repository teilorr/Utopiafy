from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Optional,
    Union
)

from components import ViewSubmitSuggestion
from utils.databases import LevesDatabase
from utils.databases import Suggestions
from discord.ext import commands
from utils import Configs
import datetime as dt
import discord

if TYPE_CHECKING:
    from core import Utopify

class Others(commands.Cog):
    def __init__(self, bot: Utopify) -> None:
        self.bot = bot

    @commands.command(name="ideia", aliases=["sugerir", "sugestão", "suggest"], help="Faz uma sugestão para o servidor")
    async def submit_suggestion(self, ctx: commands.Context):
        view = ViewSubmitSuggestion(60, self.bot)

        out = await ctx.reply("> Para criar uma sugestão, aperte o botão abaixo e siga os passos.", view=view)
        view.response = out
        view.ctx = ctx

    @commands.command(name="deny", aliases=["reject"], help="Rejeia uma sugestão", hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def reject_ideia(self, ctx: commands.Context, id: str, *, reason: str) -> None:
        async with Suggestions() as db:
            rejected = await db.reject(id)

            s_channel: discord.TextChannel = self.bot.get_channel(Configs.suggestion_channel_id)
            s_message: discord.Message = await s_channel.fetch_message(rejected.message_id)
            s_author : discord.Member = await ctx.guild.fetch_member(rejected.user_id)
            
            embeds: list[discord.Embed] = s_message.embeds
            fields = embeds[0].fields

            embed = discord.Embed(
                title=f"A ideia de {s_author.name} foi reprovada por {ctx.author.name}", 
                description=f"\U00002b06 *** - {s_message.reactions[0].count}*** | \U00002b07 *** - {s_message.reactions[1].count} ***",
                color=discord.Color.red()
            )
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
            embed.add_field(name=fields[0].name.capitalize(), value=fields[0].value, inline=False)
            embed.add_field(name="Motivo", value=reason, inline=False)
            embed.set_footer(text=f"sID: {id} | UserID: {s_author.id} • {dt.datetime.now().strftime('%d/%m/%Y')}")
            embed.set_thumbnail(url=s_author.avatar)
            await s_message.clear_reactions()
            await s_message.edit(embed=embed)

            await ctx.send("> Sugestão reprovada com sucesso!")

    @commands.command(name="accept", help="Aceita uma sugestão", hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def accept_ideia(self, ctx: commands.Context, id: str, *, reason: str) -> None:
        async with Suggestions() as db:
            approved = await db.approve(id)

            s_channel: discord.TextChannel = self.bot.get_channel(Configs.suggestion_channel_id)
            s_message: discord.Message = await s_channel.fetch_message(approved.message_id)
            s_author : discord.Member = await ctx.guild.fetch_member(approved.user_id)

            embed = discord.Embed(
                title=f"A ideia de {s_author.name} foi aprovada por {ctx.author.name}", 
                description=f"\U00002b06 *** - {s_message.reactions[0].count}*** | \U00002b07 *** - {s_message.reactions[1].count} ***",
                color=discord.Color.green()
            )
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
            embed.set_field_at(1, name="Motivo", value=reason, inline=False)
            embed.set_footer(text=f"sID: {id} | UserID: {s_author.id} • {dt.datetime.now().strftime('%d/%m/%Y')}")
            embed.set_thumbnail(url=s_author.avatar)
            await s_message.clear_reactions()
            await s_message.edit(embed=embed)

            await ctx.send("> Sugestão aprovada com sucesso!")

    @commands.command(name="rank", help="Mostra seu nível")
    async def rank(self, ctx: commands.Context, member: Optional[discord.Member]=None) -> None:
        async with LevesDatabase() as db:
            if member:
                xp, lvl = await db.get_rank(member.id)
            else:
                xp, lvl = await db.get_rank(ctx.author.id)
            
            await ctx.send(f"> {'*' + str(member) + '*' if member else 'Você'} é ***level {lvl}*** com ***{xp}xp***")

    @commands.command(name="leaderboard", aliases=["top"], help="Leaderboard de xp do server")
    async def leaderboard(self, ctx: commands.Context) -> None:
        async with ctx.typing():
            ranks: list[dict[str, Union[int, str]]] = []
            async with LevesDatabase() as db:
                leaderboard_ids = await db.get_leaderboard_ids()
                for m_id in leaderboard_ids:
                    xp, lvl = await db.get_rank(m_id)
                    member = await ctx.guild.fetch_member(m_id)
                    ranks.append({"xp": xp, "lvl": lvl, "name": member.name})

                ranks = sorted(ranks, key=lambda x: x["xp"], reverse=True)

            msg = ""
            for pos, member in enumerate(ranks):
                msg = msg + f"***{pos + 1}. {member.get('name')}*** - *level {member.get('lvl')}, {member.get('xp')}xp*\n"

            embed = discord.Embed(
                title="Leaderboard",
                description=msg,
                color=discord.Color.brand_green()
                )

            await ctx.send(embed=embed)

    @commands.command(name="minecraft", help="Mostra informações sobre o servidor de mine")
    async def minecraft(self, ctx: commands.Context):
        await ctx.send(
            "> Para PC:\n"
            "> IP: ***pudinsutopiaanarchy.jogar.io***\n\n"

            "> Para Mobile:\n"
            "> IP: ***br-enx-13.enxadahost.com***\n"
            "> Porta: 10002\n\n"
            
            "> Versões: ***1.16.5 - 1.19.2*** *(Para PC e Mobile)*\n"
            "> Canal de ajuda: <#1031001249358819339>"
        )

    @commands.command(name="source", help="URL para o código do bot")
    async def source(self, ctx: commands.Context) -> None:
        await ctx.send("> *Source:* ***https://github.com/teilorr/Utopiafy***")

async def setup(bot: Utopify) -> None:
    cog = Others(bot)
    await bot.add_cog(cog)