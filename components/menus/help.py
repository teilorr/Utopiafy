from __future__ import annotations

from collections.abc import Mapping
from discord.ext import commands
from discord import ui 
import typing as t
import discord

T = t.TypeVar("T")

class Dropdown(ui.Select):
    def __init__(self, mapping: t.Mapping[commands.Cog, list[commands.Command]]):
        self.mapping: dict[str, list[commands.Command]] = {}
        for _, cmds in mapping.items():
            for cmd in cmds:
                self.mapping[cmd.cog_name] = cmds
        self.mapping.pop(None)

        super().__init__(
            placeholder="Escolha a categoria...", 
            min_values=1, 
            max_values=1,
            options=[
                discord.SelectOption(label=cog, value=cog) 
                for cog in self.mapping.keys()
                if not getattr(cog, "hidden", False)
            ] 
        )

    async def callback(self, interaction: discord.Interaction) -> t.Any:
        selected = self.values[0]
        commands = self.mapping[selected]
        await interaction.response.edit_message(
            content="",
            embed=discord.Embed(
                title=f"Ajuda de {selected}",
                description="".join(f"***{command.name} {command.signature}*** - *{command.help or 'Comando não documentado'}*\n" for command in commands),
                color=discord.Color.brand_green()
            )
        )

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

class HelpClass(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={})

    def get_command_signature(self, command: commands.Command) -> str:
        return f"{self.context.prefix}{command.name} {command.signature}"

    def get_command_brief(self, command: commands.Command):
        return command.short_doc or 'O Comando não está documentado'

    async def send_bot_help(self, mapping: Mapping[commands.Cog, T]):
        view = ui.View().add_item(Dropdown(mapping))
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