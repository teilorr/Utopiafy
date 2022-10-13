from __future__ import annotations
from typing import (
    TYPE_CHECKING
)

from discord.ext import commands
from utils import Suggestions
from utils import Configs
from discord import ui
import datetime as dt
import discord
import string
import random

if TYPE_CHECKING:
    from core import Utopify

class ViewSubmitSuggestion(ui.View):
    def __init__(self, timeout, bot):
        self.response: discord.Message | None = None
        self.ctx: commands.Context = None
        self.bot: Utopify = bot
        super().__init__(timeout=timeout)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.ctx.author

    @ui.button(label="Criar uma sugestão", style=discord.ButtonStyle.blurple, emoji='\U0001f4a1')
    async def create_event(self, interaction: discord.Interaction, button: discord.Button):
        button.style = discord.ButtonStyle.success
        await interaction.response.send_modal(ModalSubmitSuggestion(300, self.bot, self.ctx))
        await interaction.followup.edit_message(interaction.message.id, view=self)

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True

        await self.response.edit(view=self)

class ModalSubmitSuggestion(ui.Modal, title="Sugestão"):
    def __init__(self, timeout, bot, ctx):
        self.ctx: commands.Context = ctx
        self.bot: Utopify = bot
        super().__init__(timeout=timeout)

    def gen_suggestion_id(self, size: int, chars=string.ascii_letters+string.digits) -> str:
        return "".join((random.choice(chars) for _ in range(size)))

    suggestion_title = ui.TextInput(
        label="Título da sua ideia",
        placeholder="Digite o título da ideia aqui",
        min_length=4, 
        max_length=256
    )

    suggestion_description = ui.TextInput(
        label="Sua sugestão inovadora", 
        placeholder="Digite sua sugestão aqui",
        style=discord.TextStyle.paragraph, 
        min_length=4, 
        max_length=1024
    )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.ctx.author

    async def on_submit(self, interaction: discord.Interaction):
        s_ID = self.gen_suggestion_id(size=6)
        
        s_channel = self.bot.get_channel(Configs.suggestion_channel_id)
        embed = discord.Embed(title=f'Ideia por {interaction.user.name}', color=discord.Color.orange())
        embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
        embed.add_field(name=str(self.suggestion_title), value=str(self.suggestion_description))
        embed.set_footer(text=f"sID: {s_ID} | UserID: {interaction.user.id} • {dt.datetime.now().strftime('%d/%m/%Y')}")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)

        message = await s_channel.send(embed=embed)
        await message.add_reaction("\U00002b06")
        await message.add_reaction("\U00002b07")

        async with Suggestions() as db:
            created_idea = await db.create(s_ID, message.id, interaction.user.id)

        await interaction.response.send_message(f"Sugestão enviada com sucesso! Obrigado pela sua contribuição com o servidor.\nID da sugestão: `{created_idea.id}`", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f"Parece que um erro aconteceu durante o envio da sua sugestão para os servidores. Tente novamente mais tarte\nPor favor, envie essas informações aos desenvolvedores: ```{', '.join(error.args)}```", ephemeral=True)

