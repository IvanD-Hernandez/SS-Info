#!/usr/bin/env python3

import os
import discord
import asyncpg
from discord.ext import commands
from dotenv import load_dotenv

import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


DATABASE_URL = os.getenv('DATABASE_URL')
print("Connecting to:", DATABASE_URL)
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Connecting to:", DATABASE_URL)

    bot.db_pool = await asyncpg.create_pool(DATABASE_URL)


    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{bot.user} is connected to guild: {guild.name} (id: {guild.id})'
    )

@bot.event
async def on_member_join(member):
    guild = member.guild
    role = "Minnow"

    role = discord.utils.get(guild.roles, name=role)

    if role:
        await member.add_roles(role)
        print(f"Assigned role '{role.name}' to {member.name}")
    else:
        print(f"Role '{role}' not found in guild '{guild.name}'")

    welcome_channel = "welcome"
    channel = discord.utils.get(guild.text_channels, name=welcome_channel)
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}! 🎉")

@bot.command(name="hlookup")
async def houseLookup(ctx, house:str):
    async with bot.db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT student_name, ss_ranking FROM users WHERE affiliation = $1 ORDER BY ss_ranking DESC;",house)
        if rows:
            msg = "\n".join([f"{r['student_name']} — {r['ss_ranking']} Stars" for r in rows])
            await ctx.send(f"**Ranking for House {house}:**\n{msg}")
        else:
            await ctx.send(f"There doesnt appear to be a House/Team that goes by {house}...")

@bot.command(name="hello")
async def hello_command(ctx):
    """Bot says hello to the user."""
    await ctx.send(f"Hello, {ctx.author.mention}!")


bot.run(TOKEN)
