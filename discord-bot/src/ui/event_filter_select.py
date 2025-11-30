from __future__ import annotations

from typing import List

from ui.template.discord_window import WindowTemplate
import discord

class EventSelector(discord.ui.Select):
    def __init__(self, rows):
        self.event_names: dict[int, str] = {}
        options = self._rows_to_options(rows)
        super().__init__(
            placeholder="Select an event to trigger",
            min_values=1,
            max_values=1,
            options=options,
        )
        
        
    def _rows_to_options(self, rows):
        options = [
            discord.SelectOption(
                label=row["post_title"],
                value=row["id"],
            )
            for row in rows
        ]
        self.event_names = {
            option.value: option.label for option in options
        }
        return options

    def update_options(self, rows):
        self._rows_to_options(rows)


    async def callback(self, interaction: discord.Interaction):
        event_id = int(self.values[0])
        parent: "EventSelect" = self.view 
        print(self.event_names)
        await parent.on_selection(interaction, self.event_names[event_id],event_id)



class EventSelect(discord.ui.View):
    def __init__(
            self, 
            guild: discord.Guild,
            author_id: int,
            service_handler,
            button_config,
        ):
        super().__init__(timeout=180)  
        self.handler = service_handler
        self.author_id = author_id
        self.guild = guild
        self.button_cfg = button_config
        self.event_select: EventSelector | None = None
        self.selected_event: int | None = None
        self.selected_ids: List[int] | None = None
        self.emojis = {}
        self.resolve_emojis()
  
    async def _build_embed(self) -> discord.Embed:

        if self.selected_ids:
            rows = await self.handler.get_event_participants(self.selected_ids)
        else:
            rows = None

        if not self.selected_event:
            title = "Event – No Event Selected"
        else:
            title = "Event – " + self.selected_event

        if rows:
            print(rows)
            # "\n".join(f"{i+1}. {r['student_name']} — {r['ss_ranking']}" for i, r in enumerate(rows))
            desc = "\n".join(f"{i+1}. {self.emojis[r['affiliation']]} {r['student_name']}" for i,r in enumerate(rows))
        else:
            desc = "*No participants to display*"



        embed = discord.Embed(title=title,description=desc)
        return embed

    async def on_selection(self, interaction, event_name: str, event_id: str):
        self.selected_event = event_name
        row = await self.handler.get_events(event_id)
        if len(row) == 1:
            self.selected_ids = row[0]["participants"]

        await self._refresh(interaction)


    async def _create_selects(self):
        rows = await self.handler.get_events()
        self.event_select = EventSelector(rows)
        self.add_item(self.event_select)

    async def _refresh(self, interaction: discord.Interaction):
        embed = await self._build_embed()
        await interaction.response.edit_message(embed=embed,view=self)

    def resolve_emojis(self):
        for idx, (key, cfg) in enumerate(self.button_cfg.items()):
            if "emoji_name" in cfg:
                found = discord.utils.get(self.guild.emojis, name=cfg["emoji_name"])
                if found:
                    self.emojis[key] = found
                    continue
            self.emojis[key] = cfg.get("fallback", "❔")


    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "Only the person who ran this command can use these buttons.",
                ephemeral=True,
            )
            return False
        return True