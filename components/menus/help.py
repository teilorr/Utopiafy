from __future__ import annotations

from discord.ext import commands
from discord import ui 
import typing as t
import discord

T = t.TypeVar("T")

class Dropdown(ui.Select):
    def __init__(self, mapping: t.Mapping[commands.Cog, list[commands.Command]], help_class: "HelpClass"):
        self.help_class = help_class
        self.mapping = mapping

        super().__init__(
            placeholder="Escolha a categoria...", 
            min_values=1, 
            max_values=1,
            options=[
                discord.SelectOption(label=cog.qualified_name, value=cog.qualified_name) 
                for cog in mapping.keys()
                if not getattr(cog, "hidden", False) and cog
            ]
        )

    async def create_message_for(self, cog: commands.Cog) -> list[str]:
        result: list[str] = []
        for cmd in await self.help_class.filter_commands(cog.get_commands()):
            result.append(f"***{self.help_class.get_command_signature(cmd)}*** - *{self.help_class.get_command_brief(cmd)}*")

        return result

    async def callback(self, interaction: discord.Interaction) -> t.Any:
        selected = self.values[0]

        cog = self.help_class.context.bot.get_cog(selected)
        msg = await self.create_message_for(cog)

        embed = discord.Embed(
            title=f"{selected}",
            description=cog.description,
            color=discord.Color.greyple()
        )
        embed.add_field(name=f"Visualizando `{len(msg)}` comandos", value="\n".join(msg))
        await interaction.response.edit_message(
            content="",
            embed=embed
        )

class HelpClass(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={})

    def get_command_signature(self, command: commands.Command) -> str:
        return f"{self.context.prefix}{command.name} {command.signature}"

    def get_command_brief(self, command: commands.Command):
        return command.short_doc or 'O Comando não está documentado'

    async def send_bot_help(self, mapping: t.Mapping[commands.Cog, list[commands.Command]]):
        view = ui.View().add_item(Dropdown(mapping, self))
        channel = self.get_destination()
        await channel.send(
            content="> Selecione uma das categorias abaixo para visualizar os comandos relacionados",
            view=view
        )

    async def send_command_help(self, command: commands.Command):
        channel = self.get_destination()
        embed = discord.Embed(title=self.get_command_signature(command), color=discord.Color.blurple())
        embed.add_field(name='Função', value=f'`{command.help or "O Comando não está documentado!"}`')
        alias = command.aliases
        if alias:
            embed.add_field(name='Ou se preferir...', value=", ".join(alias), inline=False)

        await channel.send(embed=embed)

    async def send_error_message(self, error: str):
        embed = discord.Embed(title='Error', description=error, color=discord.Color.red())
        channel = self.get_destination()
        await channel.send(embed=embed)