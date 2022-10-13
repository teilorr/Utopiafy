from __future__ import annotations
from typing import (
    TYPE_CHECKING
)

from discord.ext import commands
from discord.ext import menus
import discord

import datetime as dt

if TYPE_CHECKING:
    from core import Utopify
    from utils.databases.warns import Warn

class MySource(menus.ListPageSource):
    def __init__(self, entries: list[Warn], bot: Utopify, ctx: commands.Context, **kwargs) -> None:
        super().__init__(entries, **kwargs)
        self.bot = bot
        self.ctx = ctx

    async def format_page(self, menu: "WarnsMenuPages", entries: list[Warn]):
        embed = discord.Embed(
            title=f"Warns - `{menu.current_page + 1}/{self.get_max_pages()}`",
            color=discord.Color.orange()
        )
        embed.set_footer(text=f"{self.ctx.author} • {dt.datetime.now():%d/%m/%Y}")
        embed.add_field(
            name=f"*Mostrando `{len(entries)}` warns* \n", 
            value=
                "\n".join([
                    f"*`ID: {warn.warn_id}`* - "
                    f"*{warn.reason} - "
                    f"{discord.utils.format_dt(warn.warned_at, 'd')}" 
                    f"({discord.utils.format_dt(warn.warned_at, 'R')}. " 
                    f"Autor: {(await self.ctx.guild.fetch_member(warn.author_id)).mention})*"
                    for warn in entries
                ])
            )
        return embed

class WarnsMenuPages(discord.ui.View, menus.MenuPages):
    def __init__(self, source) -> None:
        super().__init__(timeout=60)
        self._source: MySource = source
        self.current_page: int = 0
        self.ctx: commands.Context = None
        self.message: discord.Message = None

    async def start(self, ctx: commands.Context, *, channel=None, wait=False):
        await self._source._prepare_once()
        self.message = await self.send_initial_message(ctx, ctx.channel)
        self.ctx = ctx

    async def _get_kwargs_from_page(self, page):
        value = await super()._get_kwargs_from_page(page)
        if "view" not in value:
            value.update({"view": self})
        return value
    
    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author

    @discord.ui.button(emoji='⬅', style=discord.ButtonStyle.gray)
    async def before_page(self, interaction: discord.Interaction, _):
        await self.show_checked_page(self.current_page - 1)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(emoji='➡', style=discord.ButtonStyle.gray)
    async def next_page(self, interaction: discord.Interaction, _):
        await self.show_checked_page(self.current_page + 1)
        await interaction.response.edit_message(view=self)