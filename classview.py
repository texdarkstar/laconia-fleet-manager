from discord import Interaction, SelectOption
from discord.ui import Select, View
import ship_classes


class ClassDropdown(Select):
    def __init__(self):
        options = []
        for key in ship_classes.classes.keys():
            options.append(SelectOption(label=key, description=ship_classes.classes[key]))

        super().__init__(placeholder="Class", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(f"Picked {self.values[0]}", ephemeral=True)
        self.view.stop()


class ClassView(View):
    def __init__(self, shipname, timeout=180):
        super().__init__(timeout=timeout)
        self.shipname = shipname
        self.add_item(ClassDropdown())

