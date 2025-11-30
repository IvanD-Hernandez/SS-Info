from discord.ext import commands
import discord

class llmCog(commands.Cog, name="LLM Commands"):
    def __init__(self, bot: commands.Bot, llm_service):
        self.bot = bot
        self.manager = llm_service

    @commands.has_role("SS-Admin")
    @commands.command(name="ask", help=f"Ask the llm a question directly.")
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