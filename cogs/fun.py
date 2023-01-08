from __future__ import annotations
from typing import (
    TYPE_CHECKING
)

from discord.ext import commands
import discord

from utils.others.phrase_gen import IdeiaGenerator
from random import Random
import datetime as dt
import asyncio

from utils import Cog

random = Random()

if TYPE_CHECKING:
    from core import Utopify

class Fun(Cog, name="Diversão"):
    """:\U0001f923:""" # Descrição para mostrar no ==help
    def __init__(self, bot: Utopify) -> None:
        self.bot = bot

    @commands.command(name="xiu", help="Silencia um usuario através de votação popular")
    @commands.cooldown(1, 248, commands.BucketType.guild)
    async def xiu(self, ctx: commands.Context, member: discord.Member) -> None:
        voting: set[discord.Member] = set()
        if member.id == self.bot.owner_id:
            return ctx.command.reset_cooldown(ctx)
        
        if member.is_timed_out():
            embed = discord.Embed(title=":no_entry_sign: Calma aí, camarada!", color=discord.Color.red())
            embed.add_field(name="Que sangue é esse!", value="Vocês odeiam este sujeito ao ponto de silenciá-lo *duas* vezes?", inline=False)
            await ctx.reply(embed=embed, mention_author=False, delete_after=15)
            ctx.command.reset_cooldown(ctx)
            return

        embed = discord.Embed(title=f"À helieia, meus amigos! {ctx.author.name} iniciou uma votação para silenciar {member.name} por cinco minutos!", color=discord.Color.orange())
        embed.add_field(name="Que os jogos comecem!", value=f"Faltam 2 minutos até o final da votação, cinco votos são nescessários para silenciar {member.name}.", inline=False)
        msg = await ctx.send(embed=embed, reference=ctx.message, delete_after=120)
        await msg.add_reaction('\U0001f507')

        def check(r: discord.Reaction, u: discord.Member):
            if r.message.id == msg.id and str(r.emoji) == '\U0001f507':
                voting.add(u)
                return len(voting) == 5

        try:
            await self.bot.wait_for('reaction_add', check=check, timeout=120)
        except asyncio.TimeoutError:
            await ctx.send(f"> Vocês não tiveram votos o suficiente para silenciar *{member.name}*", delete_after=5)
        else:
            if len(voting) == 5:
                await member.timeout(dt.timedelta(minutes=5))
            
                embed = discord.Embed(title=f"Vitória do povo brasileiro, viva a democracia!", color=discord.Color.green())
                embed.add_field(name="Se fudeu, o governo venceu!", value=f"Por votação popular, {member.mention} foi silenciado!", inline=False)
                await ctx.send(embed=embed, reference=ctx.message, delete_after=15)

    @commands.command(name="bitches", help="bitches?")
    async def bitches(self, ctx: commands.Context) -> None:
        random_number = random.random()
        if ctx.author.id in {360153969432985628, 852643106482683934, 80236417579994318, 931930984486699039}:
            return await ctx.send('vai se fuder, vc n tem bitches')

        if random_number > 0.5:
            await ctx.send('Não, você claramente não tem bitches \U0001f4e1 bitches \U0001f4e1 bitches \U0001f4e1 bitches \U0001f4e1 bitches')
        else:
            await ctx.send('VOCÊ TEM BITCHES')

    @commands.command(name="gay", help="Já se perguntou o quão gay você é?")
    async def gay(self, ctx: commands.Context) -> None:
        await ctx.send(f"> *{ctx.author}* é {random.randint(0, 100)}% gay")

    @commands.command(name="jogo", help="Gera uma ideia de jogo muito louca!")
    async def game_ideia(self, ctx: commands.Context, member: discord.Member=None) -> None:
        gen = IdeiaGenerator()
        await ctx.send(f"> {gen.generate(member.display_name if member else ctx.author.display_name)}")
        
    @commands.command(name="8ball", help="Faça uma pergunta e a bola mágica te responderá.")
    async def eightball(self, ctx: commands.Context, *, _: str) -> None:
        answers = {
            "affirmative": [
                "Certamente",
                "Com certeza sim",
                "Sem dúvidas!",
                "Definitivamente sim",
                "Pode ter certeza que sim",
                "Da forma que eu vejo a situação, sim",
                "Provavelmente sim",
                "Sim",
                "Sinais me dizem que sim"
            ],
            "neutral": [
                "O futuro é nebuloso",
                "Me pergunte novamente mais tarde...",
                "Melhor não te falar agora",
                "Não consigo prever isso agora",
                "Se concetre e pergunte novamente"
            ],
            "negative": [
                "Não conte com isso",
                "Minha resposta é não",
                "Minhas fontes dizem que não",
                "Claro que não!",
                "Eu tenho minhas dúvidas"
            ]
        }
        category = answers.get(random.choice(list(answers.keys())))
        answer = category[random.randint(0, len(category) - 1)]
        await ctx.reply(f"> {answer}")

async def setup(bot: Utopify) -> None:
    cog = Fun(bot)
    await bot.add_cog(cog)