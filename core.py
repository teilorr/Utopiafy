from utils import DotEnv, Configs
from components import HelpClass
from discord.ext import commands
import discord
import pathlib
import asyncio

on_development = False

class Utopify(commands.Bot):
    def __init__(self) -> None:
        self.utopia: discord.Guild = None
        self.on_development = on_development
        super().__init__(
            command_prefix=commands.when_mentioned_or("=="),
            case_insensitive=True,
            intents=discord.Intents.all(),
            strip_after_prefix=True,
            help_command=HelpClass(),
            activity=discord.Game(name="Em busca do Utopia Automático"),
            status=discord.Status.idle if on_development else discord.Status.online,
        )

    async def setup_hook(self) -> None:
        for file in pathlib.Path("./cogs").glob("**/[!_]*.py"):
            extension = ".".join(file.parts) \
                           .removesuffix(".py")
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(e)

        self.owner_id = Configs.owner_id
        self.logs_channel = await self.fetch_channel(Configs.logs_channel_id)
        self.errors_channel = await self.fetch_channel(Configs.errors_channel_id)

        await self.ready_once() # will block the setup_hook until the bot is ready

    async def on_ready(self) -> None:
        print(f"{self.user}/{self.user.id} online")

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

utopify = Utopify()
utopify.run(DotEnv.get("TOKEN"), log_level=40)