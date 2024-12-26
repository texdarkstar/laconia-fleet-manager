from discord import Interaction, SelectOption
from discord.ui import Select, View
# import ship_classes


class ClassDropdown(Select):
    def __init__(self, fleetmanager):
        options = []
        self.fleetmanager = fleetmanager
        # if not fleetmanager:
        #     for key in ship_classes.classes.keys():
        #         options.append(SelectOption(label=key, description=ship_classes.classes[key]))

        for key in self.fleetmanager.ship_models.keys():
            options.append(SelectOption(label=key, description=self.fleetmanager.ship_models[key]))

        super().__init__(placeholder="Class", min_values=1, max_values=1, options=options)


    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(f"Picked {self.values[0]}", ephemeral=True)
        self.view.stop()


class ClassView(View):
    def __init__(self, name, fleetmanager, timeout=180):
        super().__init__(timeout=timeout)
        self.fleetmanager = fleetmanager
        self.name = name
        self.add_item(ClassDropdown(self.fleetmanager))

