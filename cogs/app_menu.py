from __future__ import annotations
import typing as t

from utils import WarningsDatabase
from utils import Configs
from utils import Cog

from discord import app_commands
import discord

import datetime as dt

if t.TYPE_CHECKING:
    from core import Utopify

class AppMenuCog(Cog, hidden=True):
    def __init__(self, bot: Utopify) -> None:
        self.bot = bot
        self._commands: t.List[t.Union[app_commands.ContextMenu, app_commands.Command]] = [
            app_commands.ContextMenu(
                name="Ver informações",
                type=discord.AppCommandType.user,
                callback=self.user_info
            ),
            app_commands.ContextMenu(
                name="Reportar",
                type=discord.AppCommandType.message,
                callback=self.report_message
            ),
            app_commands.Command(
                name="report",
                description="Reporta um usuário pra staff do servidor",
                callback=self.report_user
            )
        ]

    async def report_user(self, interaction: discord.Interaction, user: discord.Member, reason: str) -> None:
        await interaction.response.send_message(f"{user.display_name}#{user.discriminator} foi reportado com sucesso!", ephemeral=True)

        report_channel = interaction.guild.get_channel(Configs.report_channel_id)
        embed = discord.Embed(
            description=
                f"***\U0001f50e Reportado***: {user.mention} *({user.id})*\n"
                f"***\U00000023 Canal***: {interaction.channel.mention}\n"
            ,
            color=0xFFFFFF # branco
        )
        embed.add_field(name="Motivo", value=f"```{reason}```")
        embed.set_author(name=f"Autor do report: {interaction.user.name} ({interaction.user.id})")
        embed.timestamp = dt.datetime.now()

        logs_msg = await report_channel.send(embed=embed)
        
        await logs_msg.add_reaction("\U0001f7e9") # quadrado verde
        await logs_msg.add_reaction("\U0001f7e7") # quadrado laranja
        await logs_msg.add_reaction("\U0001f7e5") # quadrado vermelho
        await logs_msg.add_reaction("\U00002b1c") # quadrado branco
        await logs_msg.add_reaction("\U0001f5d1") # lixeira

    async def report_message(self, interaction: discord.Interaction, message: discord.Message) -> None:
        await interaction.response.send_message(f"{message.author.display_name}#{message.author.discriminator} foi reportado com sucesso!", ephemeral=True)

        attachments = "\n\n".join(attachment.url for attachment in message.attachments)
        report_channel = interaction.guild.get_channel(Configs.report_channel_id)
        embed = discord.Embed(
            description=
                f"***\U0001f50e Reportado***: {message.author.mention} *({message.author.id})*\n"
                f"***\U0001f4dc Motivo***: [Ver mensagem]({message.jump_url})\n"
                f"***\U00000023 Canal***: {message.channel.mention}\n"
            ,
            color=0xFFFFFF # branco
        )
        embed.add_field(name="Conteúdo da mensagem", value=f"```{message.content or attachments}```")
        embed.set_author(name=f"Autor do report: {interaction.user.name} ({interaction.user.id})")
        embed.timestamp = dt.datetime.now()

        logs_msg = await report_channel.send(embed=embed)
        
        await logs_msg.add_reaction("\U0001f7e9") # quadrado verde
        await logs_msg.add_reaction("\U0001f7e7") # quadrado laranja
        await logs_msg.add_reaction("\U0001f7e5") # quadrado vermelho
        await logs_msg.add_reaction("\U00002b1c") # quadrado branco
        await logs_msg.add_reaction("\U0001f5d1") # lixeira

    async def user_info(self, interaction: discord.Interaction, member: discord.Member) -> None:
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
    for command in cog._commands:
        bot.tree.add_command(command)

    await bot.add_cog(cog)