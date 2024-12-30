from ui import *
from discord import Interaction, SelectOption
from discord.ui import Select, View, Button
from secret import *


class SubmitButton(Button):
    def __init__(self, fleetmanager):
        self.fleetmanager = fleetmanager

        super().__init__(label="Register")


    async def callback(self, interaction: Interaction):
        if self.view.shipyard_ready and self.view.model_ready:
            self.view.stop()

        elif not self.view.shipyard_ready:
            await interaction.response.send_message("Please select a shipyard.", ephemeral=True, )

        elif not self.view.model_ready:
            await interaction.response.send_message("Please select a model.", ephemeral=True, )


class RegisterView(View):
    def __init__(self, fleetmanager, timeout=180):
        super().__init__(timeout=timeout)
        self.fleetmanager = fleetmanager
        self.shipyard_ready = False
        self.model_ready = False

        self.add_item(ModelDropdown(self.fleetmanager))
        self.add_item(ShipyardDropdown(self.fleetmanager))
        self.add_item(SubmitButton(self.fleetmanager))
