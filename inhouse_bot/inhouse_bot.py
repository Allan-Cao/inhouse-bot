import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv() # Loads .env variables

intents = discord.Intents.default()
test_servers = [821109702162907158]

class InhouseBot(commands.Bot):
    def __init__(self):
        super().__init__(intents=intents, debug_guilds=test_servers)
        from inhouse_bot.cogs.queue_cog import queue_cog
        from inhouse_bot.cogs.admin_cog import admin_cog
        from inhouse_bot.cogs.info_cog import info_cog
        from inhouse_bot.cogs.registration_cog import registration_cog

        self.add_cog(queue_cog(self))
        self.add_cog(admin_cog(self))
        self.add_cog(info_cog(self))
        self.add_cog(registration_cog(self))

    async def on_ready(self):
        print(f"We have logged in as {self.user.name}")
        print(f"We are in {len(self.guilds)} guilds")
        # change discord status to playing "Inhouse Queues"
        await self.change_presence(activity=discord.Game(name="Inhouse Queues"))

    def run(self):
        super().run(os.getenv("SERA_TOKEN"))
