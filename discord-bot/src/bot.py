#!/usr/bin/env python3

import os
import discord
import asyncpg
from discord.ext import commands
from dotenv import load_dotenv
from services.ss_service import StarSystem

import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
DATABASE_URL = os.getenv('DATABASE_URL')

class SS_Info(commands.Bot):
    async def setup_hook(self):
        print("Connecting to:", DATABASE_URL)
        self.db_pool = await asyncpg.create_pool(DATABASE_URL)

        self.services = {
            "star_system": StarSystem(self.db_pool)
        }

        await self.load_extension("cogs.star_system")




    async def close(self):
        await super().close()
        await self.db_pool.close()



# @bot.command(name="hello")
# async def hello_command(ctx):
#     """Bot says hello to the user."""
#     await ctx.send(f"Hello, {ctx.author.mention}!")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = SS_Info(command_prefix="!", intents=intents, case_insensitive=True)
bot.run(TOKEN)
