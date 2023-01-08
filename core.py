# // ---- O código não é um dos melhores, siga por sua conta e risco! ----- //
from __future__ import annotations

from utils import DotEnv, Configs
from components import HelpClass
from discord.ext import commands
import discord
import pathlib
import asyncio

class Utopify(commands.Bot):
    def __init__(self) -> None:
        self.utopia: discord.Guild = None
        super().__init__(
            command_prefix="==",
            case_insensitive=True,
            strip_after_prefix=True,
            help_command=HelpClass(),
            intents=discord.Intents.all(),
            activity=discord.Game(name="Em busca do Utopia Automático"),
            allowed_mentions=discord.AllowedMentions(
                everyone=False,
                roles=False,
                users=True,
            )
        )

    async def ready_once(self):
        def error_handler(task: asyncio.Task):
            exc = task.exception()
            if exc:
                print(exc)

        async def run_once_when_ready():
            await self.wait_until_ready()

            self.utopia = self.get_guild(Configs.utopia_id) 

        ready_task = asyncio.create_task(run_once_when_ready())
        ready_task.add_done_callback(error_handler)

    async def setup_hook(self) -> None:
        # // Carrega todos os arquivos terminados em .py, menos os que começam com "_"
        for file in pathlib.Path("./cogs").glob("**/[!_]*.py"):
            extension = ".".join(file.parts) \
                           .removesuffix(".py")
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(e)

        # // Utils
        self.owner_id = Configs.owner_id
        self.logs_channel = await self.fetch_channel(Configs.logs_channel_id)
        self.errors_channel = await self.fetch_channel(Configs.errors_channel_id)

        # // NOTE: Vai bloquear *setup_hook* até que o bot fique pronto
        await self.ready_once()

    async def on_ready(self) -> None:
        print(f"{self.user}/{self.user.id} online")

utopify = Utopify()
utopify.run(DotEnv.get("TOKEN"), log_level=40)