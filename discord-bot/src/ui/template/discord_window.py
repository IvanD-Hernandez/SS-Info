from __future__ import annotations

from typing import Optional, Sequence, Dict, Any

import discord

# Meant to be inherited, not stand alone.
class WindowTemplate(discord.ui.View):
    def __init__(
            self, 
            _author_id: int, 
            _guild: discord.Guild,
            _button_config,
            _page_size: int = 10,
            timeout: Optional[float] = 180,
        ):
        super().__init__(timeout=180)

        self.author_id = _author_id
        self.guild = _guild
        self.active_selections: set[str] = set()
        self.page: int = 0
        self.page_size: int = _page_size  
        self.button_cfg = _button_config
        self.button_list = []
        self.emojis = {}
        self._create_buttons()

            
    # Must be implemented by inheritor
    async def _build_embed(self) -> discord.Embed:

        raise NotImplementedError
    
    async def _get_current_selections(self) -> Optional[Sequence[str]]:
        return list(self.active_selections) if self.active_selections else None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "Only the person who ran this command can use these buttons.",
                ephemeral=True,
            )
            return False
        return True
    
    async def _refresh(self, interaction: discord.Interaction):
        raise NotImplementedError

    async def _toggle_selection(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button,
            button_id: str,
    ):
        if button_id in self.active_selections:
            self.active_selections.remove(button_id)
            button.style = discord.ButtonStyle.secondary
        else:
            self.active_selections.add(button_id)
            button.style = discord.ButtonStyle.success

        self.page = 0
        await self._refresh(interaction)

    def _resolve_emoji(self, cfg: Dict[str, Any]):
        fallback = cfg.get("fallback", "❔")
        if self.guild is None:
            return fallback

        if "emoji_name" in cfg:
            found = discord.utils.get(self.guild.emojis, name=cfg["emoji_name"])
            if found:
                return found

        if "emoji_id" in cfg:
            print("found")
            found = discord.utils.get(self.guild.emojis, name=cfg["emoji_id"])
            if found:
                return found

        return fallback

    def _create_buttons(self):
        pass