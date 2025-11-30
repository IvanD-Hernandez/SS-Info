from __future__ import annotations

from ui.template.discord_window import WindowTemplate
import discord



class NameFilterView(WindowTemplate):
    def __init__(
            self, 
            guild: discord.Guild,
            author_id: int,
            service_handler,
            button_config,
        ):
        self.handler = service_handler
        super().__init__(
            _author_id=author_id,
            _guild=guild,
            _button_config=button_config,
            _page_size=10,
        )

        
    async def _build_embed(self) -> discord.Embed:

        _selection = await self._get_current_selections()
 
        total = await self.handler.count_names(_selection)
        print(f"current selections: {_selection}")

        max_page = max((total - 1) // self.page_size, 0) if total > 0 else 0

        if self.page > max_page:
            self.page = max_page
        if self.page < 0:
            self.page = 0

        rows = await self.handler.get_names(
            house=_selection,
            page=self.page,
            page_size=self.page_size
        )
        if rows:
            print(rows)
            # "\n".join(f"{i+1}. {r['student_name']} — {r['ss_ranking']}" for i, r in enumerate(rows))
            desc = "\n".join(f"{i+1}. {self.emojis[r['affiliation']]} {r['student_name']} - {r['ss_ranking']} Stars" for i,r in enumerate(rows))
        else:
            desc = "*No results for this filter.*"

        if not self.active_selections:
            title = "Names – All Students"
        else:
            labels = []
            for key in sorted(self.active_selections):
                labels.append(key)
            title = "Names – " + ", ".join(labels)

        embed = discord.Embed(title=title,description=desc)
        embed.set_footer(
            text=f"Page {self.page + 1} / {max_page + 1 if total > 0 else 1} • {total} total"
        )
        return embed

    async def _refresh(self, interaction: discord.Interaction):
        embed = await self._build_embed()
        await interaction.response.edit_message(embed=embed,view=self)

    def _create_buttons(self):
        
        for idx, (key, cfg) in enumerate(self.button_cfg.items()):
            print(cfg)
            _emoji = self._resolve_emoji(cfg)
            self.emojis[key] = _emoji
            _row = cfg.get("row",0)

            _button = discord.ui.Button(
                emoji=_emoji,
                label="",
                style=discord.ButtonStyle.secondary,
                row=_row
            )

            async def _callback(
                    interaction: discord.Interaction,
                    button: discord.ui.Button = _button,
                    button_id: str = key,
            ):
                await self._toggle_selection(interaction,button,button_id)
            

            _button.callback = _callback
            self.add_item(_button)
            self.button_list.append(_button)

        refresh_button = discord.ui.Button(
            emoji="🔄",
            style=discord.ButtonStyle.secondary,
            row=1,
        )

        prev_button = discord.ui.Button(
            emoji="◀️",
            style=discord.ButtonStyle.secondary,
            row=1,
        )

        next_button = discord.ui.Button(
            emoji="▶️",
            style=discord.ButtonStyle.secondary,
            row=1,
        )
        async def refresh_cb(interaction: discord.Interaction, b=prev_button):
            self.active_selections.clear()

            for child in self.children:
                if isinstance(child, discord.ui.Button):
                    if child in self.button_list:
                        child.style = discord.ButtonStyle.secondary

            self.page = 0
            await self._refresh(interaction)

        async def prev_cb(interaction: discord.Interaction, b=prev_button):
            if self.page > 0:
                self.page -= 1
            await self._refresh(interaction)

        async def next_cb(interaction: discord.Interaction, b=next_button):
            self.page += 1
            await self._refresh(interaction)

        refresh_button.callback = refresh_cb
        prev_button.callback = prev_cb
        next_button.callback = next_cb

        self.add_item(refresh_button)
        self.add_item(prev_button)
        self.add_item(next_button)