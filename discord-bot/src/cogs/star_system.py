from discord.ext import commands
import discord

SS_CONFIG = [
     {"name": "Phoenix"},
     {"name": "Hufflepuff"},
     {"name": "Slytherin"},
     {"name": "Ravenclaw"},
     {"name": "Gryffindor"}
]

class starSystemCog(commands.Cog):

    def __init__(self, _bot: commands.Bot, ss_service):
        self.bot = _bot
        self.system = ss_service
        self._groups = [] 

    async def cog_load(self):
        for cfg in SS_CONFIG:
            grp = self._make_group(cfg)
            self.bot.add_command(grp)
            self._groups.append(grp)

    async def cog_unload(self):
        for g in self._groups:
            try:
                self.bot.remove_command(g.name)
            except Exception:
                pass
        self._groups.clear()

    def _make_group(self, cfg):
        house = cfg["name"]
        service = self.system

        async def _entry(ctx: commands.Context):
            await ctx.send(f"**{house}** commands: try `!{house} top`")


        grp = commands.Group(_entry,name=house.lower(), help=f"{house} commands",invoke_without_command=True)

        @grp.command(name="top", help=f"Show the top rankers for house {house}.")
        async def top(ctx):
            rows = await service.top_rankers(house)
            if not rows:
                await ctx.send(f"No {house} students found.")
                return
            msg = "\n".join(f"{i+1}. {r['student_name']} — {r['ss_ranking']}" for i, r in enumerate(rows))
            await ctx.send(f"🏆 **Top Ranker for house {house} **\n{msg}")

        return grp





async def setup(bot):
    ss_service = bot.services["star_system"]
    cog = starSystemCog(bot, ss_service)
    await bot.add_cog(cog)