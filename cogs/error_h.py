from __future__ import annotations
from typing import (
    TYPE_CHECKING
)

from difflib import get_close_matches
from discord.ext import commands
import discord

from utils import Cog

if TYPE_CHECKING:
    from core import Utopify

class ErrorHandler(Cog, hidden=True):
    def __init__(self, bot: Utopify) -> None:
        self.bot = bot
        self.hidden = True

    @commands.Cog.listener(name="on_command_error")
    async def on_command_error(self, ctx: commands.Context, error):
        cmd = ctx.command

        if isinstance(error, commands.CommandNotFound):
            cmd = ctx.invoked_with
            cmds = [cmd.name for cmd in self.bot.commands]
            matches = get_close_matches(cmd, cmds)
            if matches:
                for match in matches:
                    matches = f"> {match}\n"

                await ctx.send(f"> *[ERRO]* | Comando não encontrado, talvez você queria dizer:\n {matches}")

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"> *[ERRO]* | Você não pode usar o comando porque você não tem a(s) seguinte(s) permissões: `\"{', '.join(error.missing_permissions)}\"`. Resumindo o erro, você é da plebe")
            cmd.reset_cooldown(ctx)

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"> *[ERRO]* | Calma aí camarada! O comando está no cooldown, restam `{error.retry_after:.2f}s` até o comando poder ser executado novamente")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"> *[ERRO]* | \"`{error.param.name}`\" é um argumento obrigatório, informe-o e tente novamente")
            cmd.reset_cooldown(ctx)

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"> *[ERRO]* | Não posso concluir isso porque não posso fazer o seguinte: `\"{error.missing_permissions}\"`")
            cmd.reset_cooldown(ctx)

        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f"> *[ERRO]* | Não encontrei nenhum membro chamado *{error.argument}*")
            cmd.reset_cooldown(ctx)

        else:
            embed = discord.Embed(
                color=discord.Color.red()
            ).add_field(
                name="Tivemos um erro ao executar o comando!", 
                value=f"A Seguinte mensagem é útil para o dev responsável:\n\n[Check message]({ctx.message.jump_url})\n```{', '.join(error.args)}```"
            )

            await ctx.send(embed=embed)

            params = (f"{p!r}" for p in ctx.args)
            nl = "\n"
            await self.bot.errors_channel.send(
                content=f"Error while executing *{ctx.invoked_with}* on {ctx.channel.mention} being invoked by {ctx.author.mention} using the following args:\n```{f';{nl}'.join(params)}```",
                embed=embed
            )
    
async def setup(bot: Utopify) -> None:
    cog = ErrorHandler(bot)
    await bot.add_cog(cog)