import asyncio
from discord import Interaction, SelectOption
from discord.ui import Select, View
from secret import *
from time import sleep


class ShipyardDropdown(Select):
    def __init__(self, fleetmanager):
        options = []
        self.fleetmanager = fleetmanager
        # if not fleetmanager:
        #     for key in ship_classes.classes.keys():
        #         options.append(SelectOption(label=key, description=ship_classes.classes[key]))

        for key in self.fleetmanager.shipyards.keys():
            name = self.fleetmanager.user_ids[self.fleetmanager.shipyards[key]]

            options.append(SelectOption(
                label=key,
                description="Operated by " +
                str(name) or str(self.fleetmanager.shipyards[key])
              )
             )


        super().__init__(placeholder="Shipyard", min_values=1, max_values=1, options=options)


    async def callback(self, interaction: Interaction):
        if DEBUG:
            await interaction.response.send_message(f"Picked {self.values[0]}", ephemeral=True)

        self.view.stop()


class ShipyardView(View):
    def __init__(self, fleetmanager, timeout=180):
        super().__init__(timeout=timeout)
        self.fleetmanager = fleetmanager
        # self.fleetmanager.update_user_ids()
        self.add_item(ShipyardDropdown(self.fleetmanager))

