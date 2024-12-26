from discord import Interaction, SelectOption
from discord.ui import Select, View
# import ship_classes
from secret import *


class ModelDropdown(Select):
    def __init__(self, fleetmanager):
        options = []
        self.fleetmanager = fleetmanager
        for model_name in self.fleetmanager.ship_models.keys():
            classification = self.fleetmanager.ship_models[model_name]['classification']
            options.append(SelectOption(label=model_name, description=classification))

        super().__init__(placeholder="Class...", min_values=1, max_values=1, options=options)


    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
