from discord import Interaction, SelectOption
from discord.ui import Select, View
from secret import *


class ShipyardDropdown(Select):
    def __init__(self, fleetmanager):
        options = []
        self.fleetmanager = fleetmanager
        shipyards = self.fleetmanager.db.table("shipyards").select("*").execute().data

        for row in shipyards:
            owner = self.fleetmanager.return_user(row["owner"])

            options.append(SelectOption(
                label=row["name"],
                description="Operated by " + owner.display_name)
              )


        super().__init__(placeholder="Shipyard...", min_values=1, max_values=1, options=options)


    async def callback(self, interaction: Interaction):
        self.view.shipyard_ready = True
        await interaction.response.defer()
