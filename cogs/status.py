import discord
from discord import Interaction, app_commands
from discord.app_commands import Choice
from discord.ext import commands
from typing import List, Literal
from settings import STATUS
from utils import *


class StatusCog(commands.Cog, name="cogs.status"):
    def __init__(self, fleetmanager):
        self.fleetmanager = fleetmanager


    @app_commands.command(name="setstatus")
    async def setstatus(self, interaction: Interaction, ship_id: int, status: str):
        ship = {}

        if status not in STATUS:
            await interaction.response.send_message("Invalid status.")
            return

        # ship = get_ships_by_shipid(self.fleetmanager, ship_id)
        for _ship in self.fleetmanager.cached_tables["ships"]:
            # print(_ship)
            if int(_ship["id"]) == int(ship_id):
                ship = _ship
                break

        if ship and int(ship["registered_to"]) != int(interaction.user.id):
            await interaction.response.send_message("This ship is not registered to you.")

        elif ship and int(ship["registered_to"]) == int(interaction.user.id):
            self.fleetmanager.update_status(ship["id"], status)

            await interaction.response.send_message(f"**{ship['name']}** status updated to **{status}**")

        else:
            await interaction.response.send_message("Ship not found.")


    @setstatus.autocomplete("ship_id")
    async def autocomplete_ship_id(self, interaction: Interaction, current: str) -> List[Choice[str]]:
        # ships = get_ships_by_userid(self.fleetmanager, interaction.user.id)
        ships = []

        for _ship in self.fleetmanager.cached_tables["ships"]:
            if int(_ship["registered_to"]) == int(interaction.user.id):
                ships.append(_ship)

        return [
            app_commands.Choice(name=i["name"], value=str(i["id"]))
            for i in ships if current.lower() in i["name"].lower()
        ]

    @setstatus.autocomplete("status")
    async def autocomplete_status(self, interaction: Interaction, current: str) -> List[Choice[str]]:
        return [
            app_commands.Choice(name=value, value=value)
            for value in STATUS if current.lower() in value.lower()
        ]


async def setup(fleetmanager):
    await fleetmanager.add_cog(StatusCog(fleetmanager))
