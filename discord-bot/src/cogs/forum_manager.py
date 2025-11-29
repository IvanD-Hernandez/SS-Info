import discord
from discord.ext import commands
from typing import Optional
from ui.forum_ui import NameFilterView

class forumCog(commands.Cog):
    def __init__(self, bot: commands.Bot, forum_handler):
        self.bot = bot
        self.handler = forum_handler

    @commands.command(name="select")
    async def display_list(self,ctx: commands.Context):
        
        view = NameFilterView(
            forum_handler=self.handler,
            author_id=ctx.author.id,
            guild=ctx.guild
        )

        embed = await view._build_embed()
        await ctx.send(embed=embed,view=view)

async def setup(bot: commands.Bot):
    forum_handler = bot.services["forum_handler"]
    cog = forumCog(bot,forum_handler)
    await bot.add_cog(cog)