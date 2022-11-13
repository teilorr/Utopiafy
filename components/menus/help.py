from discord.ext import commands, menus
from collections.abc import Mapping
from itertools import starmap
from discord import ui 
import datetime as dt
import discord

from typing import TypeVar

T = TypeVar("T")

class helpPageSource(menus.ListPageSource):
    def __init__(self, 
                data, 
                help_class,
                ):
        super().__init__(data, per_page=6)
        self.bot_commands: list[commands.Command] = data
        self.help_class: "HelpClass" = help_class

    def format_command_on_help(self, no, command: commands.Command):
        signature = self.help_class.get_command_signature(command)
        docs = self.help_class.get_command_brief(command)
        return f"**{signature}** - *{docs}*\n"

    async def format_page(self, menu, entries):
        today = dt.datetime.now().strftime('%d/%m/%Y')

        page = menu.current_page
        max_page = self.get_max_pages()

        iterator = starmap(self.format_command_on_help, enumerate(entries, start=page * self.per_page + 1))
        page_content = ''.join(iterator)

        embed = discord.Embed(title=f'Help - `{page + 1}/{max_page}`',
                              color=discord.Color.brand_green())
        embed.add_field(name=f'Total de comandos no bot: `{len(self.bot_commands)}`', value=page_content)
        embed.set_footer(text=f'{menu.ctx.author} • {today}  ', icon_url=menu.ctx.author.avatar)
        return embed 

class menuPages(ui.View, menus.MenuPages):
    def __init__(self, source: menus.ListPageSource, *, delete_message_after: bool=False):
        super().__init__(timeout=60)
        self.delete_message_after: bool = delete_message_after
        self._source: menus.ListPageSource = source
        self.message: discord.Message | None = None
        self.ctx: commands.Context | None = None
        self.current_page: int | None = 0

    async def start(self, ctx: commands.Context, *, channel=None, wait=False):
        await self._source._prepare_once()
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, ctx.channel)

    async def _get_kwargs_from_page(self, page):
        value = await super()._get_kwargs_from_page(page)
        if 'view' not in value:
            value.update({'view': self})
        return value

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user == self.ctx.author

    @ui.button(emoji='⬅', style=discord.ButtonStyle.grey, custom_id='left')
    async def before_page(self, interaction: discord.Interaction, _):
        await self.show_checked_page(self.current_page - 1)
        await interaction.response.edit_message(view=self)

    @ui.button(emoji='➡', style=discord.ButtonStyle.grey, custom_id='right')
    async def next_page(self, interaction: discord.Interaction, _):
        await self.show_checked_page(self.current_page + 1)
        await interaction.response.edit_message(view=self)

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
        usable_commands: list[commands.Command] = []
        for cog in mapping.keys():
            try:
                for command in cog.walk_commands():
                    if not command.hidden:
                        usable_commands.append(command)
            except AttributeError: # NoneType na lista de cogs
                pass

        staff_role = self.context.guild.get_role(794460618283417613)
        formatter = helpPageSource(list(self.context.bot.commands) if staff_role in self.context.author.roles else usable_commands, self)
        menu = menuPages(formatter, delete_message_after=True)
        
        await menu.start(self.context)

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