from __future__ import annotations

from typing import Optional, Sequence, Dict, Any

import discord

def resolve_custom_emoji(
    guild: discord.Guild,
    *,
    name: Optional[str] = None,
    emoji_id: Optional[int] = None,
    fallback: str = "❔",
):
    if guild is None:
        return fallback

    if name:
        found = discord.utils.get(guild.emojis, name=name)
        if found:
            return found

    if emoji_id:
        print("found")
        found = discord.utils.get(guild.emojis, id=emoji_id)
        if found:
            return found

    return fallback

class NameFilterView(discord.ui.View):
    def __init__(
            self, 
            forum_handler, 
            author_id: int, 
            guild: discord.Guild,
            _house_config: Optional[Dict[str, Dict[str,Any]]] = None
        ):
        super().__init__(timeout=180)
        self.handler = forum_handler
        self.authorID = author_id

        self.active_selections: set[str] = set()
        self.page: int = 0
        self.page_size: int = 10

        if _house_config is None:
            _house_config = {
                "Phoenix": {
                    "label": "Phoenix",
                    "emoji": resolve_custom_emoji(
                        guild,
                        name="house_phoenix",
                        fallback="🐦‍🔥",
                    ),
                },
                "Slytherin": {
                    "label": "Slytherin",
                    "emoji": resolve_custom_emoji(
                        guild,
                        name="house_slytherin",
                        fallback="🐍",
                    ),
                },
                "Gryffindor": {
                    "label": "Gryffindor",
                    "emoji": resolve_custom_emoji(
                        guild,
                        name="house_gryffindor",
                        fallback="🦁",
                    ),
                },
                "Hufflepuff": {
                    "label": "Hufflepuff",
                    "emoji": resolve_custom_emoji(
                        guild,
                        name="house_hufflepuff",
                        fallback="🦫",
                    ),
                },
                "Ravenclaw": {
                    "label": "Ravenclaw",
                    "emoji": resolve_custom_emoji(
                        guild,
                        name="house_ravenclaw",
                        fallback="🐦‍⬛",
                    ),
                },
            }
        self.house_config = _house_config
        self.phoenix_button.emoji = self.house_config["Phoenix"]["emoji"]     
        self.slytherin_button.emoji = self.house_config["Slytherin"]["emoji"]
        self.gryffindor_button.emoji = self.house_config["Gryffindor"]["emoji"]
        self.hufflepuff_button.emoji = self.house_config["Hufflepuff"]["emoji"]
        self.ravenclaw_button.emoji = self.house_config["Ravenclaw"]["emoji"]

        self.phoenix_button.label = ""
        self.slytherin_button.label = ""
        self.gryffindor_button.label = ""
        self.hufflepuff_button.label = ""
        self.ravenclaw_button.label = ""
            

        



    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.authorID:
            await interaction.response.send_message(
                "Only the person who ran this command can use these buttons.",
                ephemeral=True,
            )
            return False
        return True
    
    async def _get_current_selections(self) -> Optional[Sequence[str]]:
        return list(self.active_selections) if self.active_selections else None
    
    async def _build_embed(self) -> discord.Embed:
        _houses = await self._get_current_selections()
        total = await self.handler.count_names(_houses)
        print(f"current selections: {_houses}")

        max_page = max((total - 1) // self.page_size, 0) if total > 0 else 0

        if self.page > max_page:
            self.page = max_page
        if self.page < 0:
            self.page = 0

        rows = await self.handler.get_names(
            house=_houses,
            page=self.page,
            page_size=self.page_size
        )
        if rows:
            print(rows)
            # "\n".join(f"{i+1}. {r['student_name']} — {r['ss_ranking']}" for i, r in enumerate(rows))
            desc = "\n".join(f"{i+1}. {r['student_name']} ({r['affiliation']})" for i,r in enumerate(rows))
        else:
            desc = "*No results for this filter.*"

        if not self.active_selections:
            title = "Names – All Students"
        else:
            labels = []
            for key in sorted(self.active_selections):
                cfg = self.house_config.get(key)
                labels.append(cfg["label"] if cfg else key)
            title = "Names – " + ", ".join(labels)

        embed = discord.Embed(title=title,description=desc)
        embed.set_footer(
            text=f"Page {self.page + 1} / {max_page + 1 if total > 0 else 1} • {total} total"
        )
        return embed
    
    async def _refresh(self, interaction: discord.Interaction):
        embed = await self._build_embed()
        await interaction.response.edit_message(embed=embed,view=self)

    async def _toggle_team(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button,
            house_key: str,
    ):
        if house_key in self.active_selections:
            self.active_selections.remove(house_key)
            button.style = discord.ButtonStyle.secondary
        else:
            self.active_selections.add(house_key)
            button.style = discord.ButtonStyle.success

        self.page = 0
        await self._refresh(interaction)

# Buttons
    @discord.ui.button(
        emoji="Phoenix", 
        style=discord.ButtonStyle.secondary,
        row=0,
    )
    async def phoenix_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await self._toggle_team(interaction, button, "Phoenix")

    @discord.ui.button(
        label="Slytherin", 
        style=discord.ButtonStyle.secondary,
        row=0,
    )
    async def slytherin_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await self._toggle_team(interaction, button, "Slytherin")

    @discord.ui.button(
        label="Gryffindor", 
        style=discord.ButtonStyle.secondary,
        row=0,
    )
    async def gryffindor_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await self._toggle_team(interaction, button, "Gryffindor")

    @discord.ui.button(
        label="Hufflepuff", 
        style=discord.ButtonStyle.secondary,
        row=0,
    )
    async def hufflepuff_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await self._toggle_team(interaction, button, "Hufflepuff")

    @discord.ui.button(
        label="Ravenclaw", 
        style=discord.ButtonStyle.secondary,
        row=0,
    )
    async def ravenclaw_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await self._toggle_team(interaction, button, "Ravenclaw")

    @discord.ui.button(
        emoji="🔄",
        style=discord.ButtonStyle.secondary,
        row=1,
    )
    async def clear_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        self.active_selections.clear()

        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if child in (self.phoenix_button, self.slytherin_button, self.gryffindor_button, self.hufflepuff_button, self.ravenclaw_button):
                    child.style = discord.ButtonStyle.secondary

        self.page = 0
        await self._refresh(interaction)

    @discord.ui.button(
        emoji="◀️",
        style=discord.ButtonStyle.secondary,
        row=1,
    )
    async def prev_page_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        if self.page > 0:
            self.page -= 1
        await self._refresh(interaction)

    @discord.ui.button(
        emoji="▶️",
        style=discord.ButtonStyle.secondary,
        row=1,
    )
    async def next_page_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        self.page += 1
        await self._refresh(interaction)


