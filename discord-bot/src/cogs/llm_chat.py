from discord.ext import commands
import discord
import traceback
import sys

class llmCog(commands.Cog):
    def __init__(self, bot: commands.Bot, llm_service):
        self.bot = bot
        self.manager = llm_service

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        full_tb = ''.join(
            traceback.format_exception(exc_type, exc_value, exc_traceback)
        )

        # Log or send it somewhere
        print("=== Full Error Traceback ===")
        print(full_tb)

        await ctx.reply("An error occurred; details were logged.")

    @commands.has_role("SS-Admin")
    @commands.command(name="ask")
    async def ask(self, ctx: commands.Context, *, prompt: str):
        print("Recieved Query")
        llm = self.manager.service

        messages = [
            {"role": "system", "content": "You are a helpful assistant in a Discord server."},
            {"role": "user", "content": prompt},
        ]

        reply = await llm.generate(messages, max_tokens=300)
        if not reply or not reply.strip():
            await ctx.reply(f"I got an empty response from the model.")
            return
            

        await ctx.reply(reply[:2000])


async def setup(bot: commands.Bot):
    llm_service = bot.services["llm_manager"]
    cog = llmCog(bot,llm_service)
    await bot.add_cog(cog)