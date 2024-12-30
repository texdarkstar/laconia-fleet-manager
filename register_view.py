from ui import *
from discord import Interaction, SelectOption
from discord.ui import Select, View, Button
from secret import *


class SubmitButton(Button):
    def __init__(self, fleetmanager):
        self.fleetmanager = fleetmanager

        super().__init__(label="Register")


    async def callback(self, interaction: Interaction):
        self.fleetmanager.update_shipyards()
        self.fleetmanager.update_ship_models()
        self.fleetmanager.update_ships()

        self.view.stop()


class RegisterView(View):
    def __init__(self, fleetmanager, timeout=180):
        super().__init__(timeout=timeout)
        self.fleetmanager = fleetmanager

        self.add_item(ModelDropdown(self.fleetmanager))
        self.add_item(ShipyardDropdown(self.fleetmanager))
        self.add_item(SubmitButton(self.fleetmanager))
