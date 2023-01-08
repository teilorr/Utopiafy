from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Optional
)

from discord.ext import commands
import discord

from utils import (
    convertToSeconds,
    WarningsDatabase,
    Configs,
)

import datetime as dt
from components.menus.show_warns import MySource, WarnsMenuPages

from utils import Cog

if TYPE_CHECKING:
    from core import Utopify

class Moderation(Cog, name="Moderação"):
    """:\U00002694:""" # Descrição para mostrar no ==help
    def __init__(self, bot: Utopify) -> None:
        self.bot = bot

    @commands.command(name="ban", help="Bane um mebro")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str="Motivo não informado") -> None:
        await member.ban(reason=reason + f" | Author: {ctx.author}")

        await ctx.send(f"> Bani *{member}* com sucesso :tada:! Lembre-se de reportar atividades esquisitas que quebram as regras usando *==report [member]*")
        await self.bot.logs_channel.send(
            embed=discord.Embed(
                description=
                    f"***\U00002702 Banido***: {member} *({member.id})*\n"
                    f"***\U0001f451 Admin***: {ctx.author} *({ctx.author.id})*\n"
                    f"***\U0001f4dc Motivo***: {reason}"
                ,
                color=discord.Color.red()
            )
            .set_footer(text=f"{ctx.author} • {dt.datetime.now():%d/%m/%Y}")
            .set_author(name=f"{member.name} foi banido por {ctx.author.name}")
        )

    @commands.command(name="unban", help="Desbane um mebro")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, member: discord.Member, *, reason: str="Motivo não informado") -> None:
        await member.unban(reason=reason + f" | Author: {ctx.author}")

        await ctx.send(f"> Desbani *{member}* com sucesso :tada:! Lembre-se de reportar atividades esquisitas que quebram as regras usando *==report [member]*")
        await self.bot.logs_channel.send(
            embed=discord.Embed(
                description=
                    f"***\U00002702 Desbanido***: {member} *({member.id})*\n"
                    f"***\U0001f451 Admin***: {ctx.author} *({ctx.author.id})*\n"
                    f"***\U0001f4dc Motivo***: {reason}"
                ,
                color=discord.Color.brand_green()
            )
            .set_footer(text=f"{ctx.author} • {dt.datetime.now():%d/%m/%Y}")
            .set_author(name=f"{member.name} foi debanido por {ctx.author.name}")
        )

    @commands.command(name="kick", help="Expula um mebro")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str="Motivo não informado") -> None:
        await member.kick(reason=reason + f" | Author: {ctx.author}")

        await ctx.send(f"> Kikei no *{member}* com sucesso :tada:! Lembre-se de reportar atividades esquisitas que quebram as regras usando *==report [member]*")
        await self.bot.logs_channel.send(
            embed=discord.Embed(
                description=
                    f"***\U00002702 Expulso***: {member} *({member.id})*\n"
                    f"***\U0001f451 Admin***: {ctx.author} *({ctx.author.id})*\n"
                    f"***\U0001f4dc Motivo***: {reason}"
                ,
                color=discord.Color.red()
            )
            .set_footer(text=f"{ctx.author} • {dt.datetime.now():%d/%m/%Y}")
            .set_author(name=f"{member.name} foi expulso por {ctx.author.name}")
        )

    @commands.command(name="mute", help="Silencia um usuário")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx: commands.Context, member: discord.Member, time: str, *, reason: str="Motivo não informado") -> None:
        on_seconds = await convertToSeconds().convert(ctx, time)

        if member.is_timed_out():
            return await ctx.send(f"> O Membro *{member}* já está silenciado")

        await member.timeout(dt.timedelta(seconds=on_seconds), reason=reason + f" | Author: {ctx.author}")
        await ctx.send(f"> Silenciei *{member}* por *{time}* com sucesso! :tada:")

        await self.bot.logs_channel.send(
            embed=discord.Embed(
                description=
                    f"***\U0001f507 Silenciado***: {member.mention} *({member.id})*\n"
                    f"***\U0001f451 Admin***: {ctx.author} *({ctx.author.id})*\n"
                    f"***\U000023f0 Tempo***: {time}\n"
                    f"***\U0001f4dc Motivo***: {reason}"
                ,
                color=discord.Color.red()
            )
            .set_footer(text=f"{ctx.author} • {dt.datetime.now():%d/%m/%Y}")
            .set_author(name=f"{member.name} foi silenciado por {ctx.author.name}")
        )

    @commands.command(name="unmute", help="Desmuta um usuário")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx: commands.Context, member: discord.Member, *, reason: str="Motivo não informado") -> None:
        if not member.is_timed_out():
            return await ctx.send(f"> O Membro *{member}* não está silenciado!")

        await member.timeout(None, reason=reason + f" | Author: {ctx.author}")
        await ctx.send(f"> Desmutei *{member}* com sucesso! :tada:")

        await self.bot.logs_channel.send(
            embed=discord.Embed(
                description=
                    f"***\U0001f507 Desmutado***: {member} *({member.id})*\n"
                    f"***\U0001f451 Admin***: {ctx.author} *({ctx.author.id})*\n"
                    f"***\U0001f4dc Motivo***: {reason}"
                ,
                color=discord.Color.brand_green()
            )
            .set_footer(text=f"{ctx.author} • {dt.datetime.now():%d/%m/%Y}")
            .set_author(name=f"{member.name} foi desmutado por {ctx.author.name}")
        )

    @commands.command(name="report", help="Reporta um usuário")
    async def report(self, ctx: commands.Context, member: discord.Member, *, reason: str) -> None:
        await ctx.message.delete()

        report_channel = ctx.guild.get_channel(Configs.report_channel_id)
        embed = discord.Embed(
            description=
                f"***\U0001f50e Reportado***: {member.mention} *({member.id})*\n"
                f"***\U0001f4dc Motivo***: [Ver mensagem]({ctx.message.jump_url})\n"
                f"***\U00000023 Canal***: {ctx.channel.mention}\n"
            ,
            color=0x00000 # preto
        )
        embed.add_field(name="Motivo", value=f"```{reason}```")
        embed.set_author(name=f"Autor do report: {ctx.author.name} ({ctx.author.id})")
        embed.timestamp = dt.datetime.now()

        await ctx.author.send(f"> *{member}* foi reportado com sucesso")
        logs_msg = await report_channel.send(embed=embed)
        
        await logs_msg.add_reaction("\U0001f7e9") # quadrado verde
        await logs_msg.add_reaction("\U0001f7e7") # quadrado laranja
        await logs_msg.add_reaction("\U0001f7e5") # quadrado vermelho
        await logs_msg.add_reaction("\U00002b1c") # quadrado branco
        await logs_msg.add_reaction("\U0001f5d1") # lixeira

    @commands.command(name="warn", help="Avisa o membro solicitado")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx: commands.Context, member: discord.Member, *, reason: str) -> None:
        async with WarningsDatabase() as db:
            warn = await db.warn(member, reason, ctx.author)
            embed = discord.Embed(
                description=
                    f"***\U0001f507 Avisado***: {member.mention} *({member.id})*\n"
                    f"***\U0001f451 Admin***: {ctx.author.mention} *({ctx.author.id})*\n"
                    f"***\U0001f4dc Motivo***: {reason or 'Nenhum motivo informado'} | [Ver mensagem]({ctx.message.jump_url})\n"
                    f"***\U0001f522 ID Do warn***: {warn.warn_id}"
                ,
                color=discord.Color.orange()
            )
            embed.set_author(name=f"{member.name} foi avisado por {ctx.author.name}")
            embed.set_footer(text=f"{ctx.author} • {dt.datetime.now():%d/%m/%Y}")

            await self.bot.logs_channel.send(embed=embed)
            await ctx.send(embed=embed)

    @commands.command(name="warnings", aliases=["warns"], help="Mostra os warns do membro solicitado")
    async def warns(self, ctx: commands.Context, member: discord.Member) -> None:
        async with WarningsDatabase() as db:
            warns = await db.get_warns_from(member)

        if warns is None:
            return await ctx.send(f"> *{member}* não tem nenhum warn!")

        async with ctx.typing():
            formatter = MySource(warns, self.bot, ctx, per_page=6)
            menu = WarnsMenuPages(formatter)
            await menu.start(ctx)

    @commands.command(name="remove_warn", aliases=["warn_remove"], help="Remove um warn baseado no id do mesmo")
    @commands.has_permissions(manage_channels=True)
    async def remove_warn(self, ctx: commands.Context, warn_id: int) -> None:
        async with WarningsDatabase() as db:
            if (removed_warn := await db.delete_warn(warn_id, ctx.guild)) is None:
                return await ctx.send("> Warn não encontrado")

            member = await self.bot.fetch_user(removed_warn.user_id)
            who_warned = await self.bot.fetch_user(removed_warn.author_id)
            
            embed = discord.Embed(
                title=f"{member} foi desavisado!",
                description=
                    f"***\U0001f507 Desavisado***: {member.mention} *({member.id})*\n"
                    f"***\U0001f451 Admin***: {who_warned.mention} *({who_warned.id})*\n"
                    f"***\U0001f4dc Motivo***: {removed_warn.reason or 'Nenhum motivo informado'}\n"
                    f"***\U0001f522 ID Do warn***: {removed_warn.warn_id}"
                ,
                color=0xff00cf
            )
            embed.set_footer(text=f"{ctx.author} • {dt.datetime.now():%d/%m/%Y}")

            await ctx.send(f"> Deletei o warn de *{member}* com sucesso", embed=embed)
            await self.bot.logs_channel.send(embed=embed)

    @commands.command(name="clear_warnings", aliases=["clear_warns"], help="Limpa os warns do membro solicitado")
    @commands.has_permissions(manage_channels=True)
    async def clear_warns(self, ctx: commands.Context, member: discord.Member) -> None:
        async with WarningsDatabase() as db:
            await db.clear_warns_from(member, current_guild=ctx.guild)
            await ctx.send(f"> Limpei os warns de *{member}* com sucesso! :tada:")

    @commands.command(name="clear", help="Limpa o chat")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, members: commands.Greedy[discord.Member], limit: commands.Range[int, 0, 100], reason: str="Motivo não informado") -> None:
        if members:
            def check(msg: discord.Message) -> bool:
                return (not members) or (msg.author in members)

            await ctx.channel.purge(limit=limit, check=check, reason=reason + f" | Author: {ctx.author}")
            await ctx.send("deletei tudo chefe")
            return

        deleted = await ctx.channel.purge(limit=limit, reason=reason + f" | Author: {ctx.author}")
        await ctx.send(f"> Limpei {len(deleted)} mensagens com sucesso")

    @commands.command(name="say")
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx: commands.Context, channel: discord.TextChannel, *, msg: str) -> None:
        await channel.send(msg)

async def setup(bot: Utopify) -> None:
    cog = Moderation(bot)
    await bot.add_cog(cog)