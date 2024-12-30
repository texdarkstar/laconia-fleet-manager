from discord import Interaction, SelectOption
from discord.ui import Select, View
# import ship_classes
from secret import *


class ModelDropdown(Select):
    def __init__(self, fleetmanager):
        options = []
        self.fleetmanager = fleetmanager
        ship_models = self.fleetmanager.db.table("ship_models").select("*").execute().data

        for row in ship_models:
            classification = row["classification"]
            model_name = row["name"]

            options.append(SelectOption(label=model_name, description=classification))


        super().__init__(placeholder="Class...", min_values=1, max_values=1, options=options)


    async def callback(self, interaction: Interaction):
        self.view.model_ready = True
        await interaction.response.defer()

