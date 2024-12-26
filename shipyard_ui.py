from discord import Interaction, SelectOption
from discord.ui import Select, View
from secret import *


class ShipyardDropdown(Select):
    def __init__(self, fleetmanager):
        options = []
        self.fleetmanager = fleetmanager
        for shipyard in self.fleetmanager.shipyards.keys():
            name = self.fleetmanager.user_ids[self.fleetmanager.shipyards[shipyard]['owner']]

            options.append(SelectOption(
                label=shipyard,
                description="Operated by " +
                str(name) or str(self.fleetmanager.shipyards[shipyard]['owner'])
              )
             )


        super().__init__(placeholder="Shipyard...", min_values=1, max_values=1, options=options)


    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
