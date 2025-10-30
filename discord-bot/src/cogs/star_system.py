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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("❌ You don’t have permission to use that command.")

    def _make_group(self, cfg):
        house = cfg["name"]
        gCmd = house.lower()
        service = self.system

        async def _entry(ctx: commands.Context):
            await ctx.send(f"**{house}** commands: try `!{house} top`")


        grp = commands.Group(_entry,name=gCmd, help=f"{house} commands",invoke_without_command=True)

        @grp.command(name="top", help=f"Show the top rankers for house {house}.")
        async def top(ctx):
            rows = await service.top_rankers(house)
            if not rows:
                await ctx.send(f"No {house} students found.")
                return
            msg = "\n".join(f"{i+1}. {r['student_name']} — {r['ss_ranking']}" for i, r in enumerate(rows))
            await ctx.send(f"🏆 **Top Ranker for house {house} **\n{msg}")

        @commands.has_role("SS-Admin")
        @grp.command(name="add", help=f"Add stars to members of House {house}.")
        async def add(ctx, _student: str = None, _num: int = None):
            if not _student or not _num:
                await ctx.send(f"⚠️ You must provide a name and amount! Usage: `!{gCmd} add <student_name> <quantity> `")
                return

            row = await service.get_student_rank(house,_student)
            if not row:
                await ctx.send(f"Could not find {_student} in House {house}.")
                return
            _new = row['ss_ranking'] + _num
            rows = await service.set_student_rank(house,_student,_new)
            if not rows:
                await ctx.send(f"Failed add {_num} stars to {_student}.")
                return
            await ctx.send(f"Congratulations {_student}! you've earn {_num} stars bring you up to {_new}!")

        @commands.has_role("SS-Admin")
        @grp.command(name="sub", help=f"Subtract stars to members of House {house}.")
        async def sub(ctx, _student: str = None, _num: int = None):
            if not _student or not _num:
                await ctx.send(f"⚠️ You must provide a name and amount! Usage: `!{gCmd} sub <student_name> <quantity> `")
                return

            row = await service.get_student_rank(house,_student)
            if not row:
                await ctx.send(f"Could not find {_student} in House {house}.")
                return
            _new = row['ss_ranking'] - _num
            rows = await service.set_student_rank(house,_student,_new)
            if not rows:
                await ctx.send(f"Failed add {_num} stars to {_student}.")
                return
            await ctx.send(f"Damn that had to hurt... {_student} lost {_num} stars, leaving them at {_new}... oof...")


        return grp





async def setup(bot):
    ss_service = bot.services["star_system"]
    cog = starSystemCog(bot, ss_service)
    await bot.add_cog(cog)