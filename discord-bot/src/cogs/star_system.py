import discord
from discord.ext import commands
from typing import Optional
from ui.name_filter_view import NameFilterView
from ui.name_filter_select import NameFilterSelect
from ui.event_filter_select import EventSelect
import traceback

_button_config = {
                "Phoenix": {
                  "emoji_name": "house_phoenix",
                    "fallback":"🐦‍🔥",
                    "row": 0
                },

                "Slytherin": {
                    "emoji_name": "house_slytherin",
                    "fallback":"🐍",
                    "row": 0
                },

                "Gryffindor": {
                    "emoji_name": "house_gryffindor",
                    "fallback":"🦁",
                    "row": 0
                },

                "Hufflepuff": {
                    "emoji_name": "house_hufflepuff",
                    "fallback":"🦫",
                    "row": 0
                },
                "Ravenclaw": {
                    "emoji_name": "house_ravenclaw",
                    "fallback":"🐦‍⬛",
                    "row": 0

                },
                "Unaffiliated": {
                    "fallback":"❔",
                    "row": 1

                }
            }

class starSystemCog(commands.Cog, name="Star System Commands"):
    def __init__(self, bot: commands.Bot, forum_handler):
        self.bot = bot
        self.handler = forum_handler
        self.selected_users: dict[int, list[int]] = {}

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        original = getattr(error, "original", error)

        # Build a full traceback string from the exception object
        tb_str = ''.join(
            traceback.format_exception(
                type(original),
                original,
                original.__traceback__
            )
        )

        # Log or send it somewhere
        print("=== Full Error Traceback ===")
        print(tb_str)

        await ctx.reply("An error occurred; details were logged.")

    # IMPLEMENT SELECTION SENDING
    @commands.command(name="select_event", help=f"Select students for forum event.")
    async def select_events(self,ctx: commands.Context):
        if ctx.guild is None:
            await ctx.send("Use this in a server, not DMs.")
            return

        view = EventSelect(
            service_handler=self.handler,
            author_id=ctx.author.id,
            guild=ctx.guild,
            button_config=_button_config,
        )
        await view._create_selects()
        embed = await view._build_embed()
        await ctx.send(embed=embed,view=view)

    # IMPLEMENT SELECTION SENDING
    @commands.command(name="select_student", help=f"Select students for forum event.")
    async def select_users(self,ctx: commands.Context):
        if ctx.guild is None:
            await ctx.send("Use this in a server, not DMs.")
            return

        view = NameFilterSelect(
            service_handler=self.handler,
            author_id=ctx.author.id,
            guild=ctx.guild,
            button_config=_button_config,
        )
        await view._create_selects()
        embed = await view._build_embed()
        await ctx.send(embed=embed,view=view)

    @commands.command(name="display", help=f"Display all students based on SS ranking.")
    async def display_list(self,ctx: commands.Context):
        if ctx.guild is None:
            await ctx.send("Use this in a server, not DMs.")
            return

        view = NameFilterView(
            service_handler=self.handler,
            author_id=ctx.author.id,
            guild=ctx.guild,
            button_config=_button_config,
        )
        embed = await view._build_embed()
        await ctx.send(embed=embed,view=view)

    @commands.has_role("SS-Admin")
    @commands.command(name="add", help=f"Add stars from a student.")
    async def add(self,ctx, _student: str = None, _num: int = None):
        if not _student or not _num:
            await ctx.send(f"⚠️ You must provide a name and amount! Usage: `!add <student_name> <quantity> `")
            return

        row = await self.handler.get_student_rank(_student)
        if not row:
            await ctx.send(f"Could not find {_student}.")
            return
        
        if len(row) > 1:
            await ctx.send(f"No can do bucko, apparently there are multiple {_student} going to this school.")
            return
        
        _new = row['ss_ranking'] + _num
        rows = await self.handler.set_student_rank(_student,_new)
        if not rows:
            await ctx.send(f"Failed add {_num} stars to {_student}.")
            return
        await ctx.send(f"Congratulations {_student}! you've earn {_num} stars bring you up to {_new}!")

    @commands.has_role("SS-Admin")
    @commands.command(name="sub", help=f"Subtract stars from a student.")
    async def sub(self, ctx, _student: str = None, _num: int = None):
        if not _student or not _num:
            await ctx.send(f"⚠️ You must provide a name and amount! Usage: `!sub <student_name> <quantity> `")
            return

        row = await self.handler.get_student_rank(_student)
        if not row:
            await ctx.send(f"Could not find {_student}.")
            return
        
        if len(row) > 1:
            await ctx.send(f"No can do bucko, apparently there are multiple {_student} going to this school.")
            return
        
        _new = row['ss_ranking'] - _num
        rows = await self.handler.set_student_rank(_student,_new)
        if not rows:
            await ctx.send(f"Failed add {_num} stars to {_student}.")
            return
        await ctx.send(f"Damn that had to hurt... {_student} lost {_num} stars, leaving them at {_new}... oof...")


async def setup(bot: commands.Bot):
    star_system = bot.services["star_system"]
    cog = starSystemCog(bot,star_system)
    await bot.add_cog(cog)