import discord
from discord import Interaction, app_commands
from discord.ext import commands
from typing import List
from settings import STATUS
from utils import *


class StatusCog(commands.Cog, name="cogs.status"):
    def __init__(self, fleetmanager):
        self.fleetmanager = fleetmanager

    @app_commands.command(name="status")
    async def status(self, interaction: Interaction, ship_id: str, status: str):
        ship = {}

        try:
            ship = get_ships_by_shipid(self.fleetmanager, ship_id)
        except CommandInvokeError:  # ship not found
            pass


        if ship and int(ship["registered_to"]) != int(interaction.user.id):
            await interaction.response.send_message("This ship is not registered to you.")

        elif ship and int(ship["registered_to"]) == int(interaction.user.id):
            self.fleetmanager.update_status(ship["id"], status)

            await interaction.response.send_message(f"**{ship['name']}** status updated to **{status}**")

        else:
            await interaction.response.send_message("Ship not found.")


    @status.autocomplete("ship_id")
    async def autocomplete(self, interaction: Interaction, current: str) -> List[app_commands.Choice[str]]:
        ships = get_ships_by_userid(self.fleetmanager, interaction.user.id)

        return [
            app_commands.Choice(name=i["name"], value=str(i["id"]))
            for i in ships if current.lower() in i["name"].lower()
        ]

    @status.autocomplete("status")
    async def autocomplete(self, interaction: Interaction, current: str) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=value, value=value)
            for value in STATUS if current.lower() in value.lower()
        ]


async def setup(fleetmanager):
    await fleetmanager.add_cog(StatusCog(fleetmanager))
