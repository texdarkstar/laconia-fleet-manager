import discord
from discord import Interaction, Member, Embed, app_commands
from discord.ext import commands
from typing import List
from ui import *
from utils import *


class RegisterCog(commands.Cog, name="cogs.register"):
    def __init__(self, fleetmanager):
        self.fleetmanager = fleetmanager


    @app_commands.command(name="register")
    async def register(self,
                       interaction: Interaction,
                       name: str, ship_model: str,
                       shipyard: str):

        if not is_fullmember(interaction.user):
            await interaction.response.send_message("Only members can register ships.", ephemeral=True)
            return

        async with interaction.channel.typing():
            embed = self.do_register(
                            interaction=interaction,
                            name=name,
                            registered_to=interaction.user,
                            ship_model=ship_model,
                            shipyard=shipyard)

            await interaction.response.send_message(embed=embed)


    @app_commands.command(name="forceregister")
    async def forceregister(self,
                            interaction: Interaction,
                            name: str, registered_to: Member,
                            ship_model: str, shipyard: str):

        if not is_officer(interaction.user):
            await interaction.response.send_message("Only Officers can register ships to members.", ephemeral=True)
            return

        async with interaction.channel.typing():
            embed = self.do_register(
                            interaction=interaction,
                            name=name,
                            registered_to=registered_to,
                            ship_model=ship_model,
                            shipyard=shipyard)


            await interaction.response.send_message(embed=embed)


    def do_register(self, interaction, name, registered_to, ship_model, shipyard):
        hull_number = new_hull(self.fleetmanager, ship_model)
        shipyard_name = get_shipyard_name_by_id(self.fleetmanager, shipyard)
        ship_model_name = get_model_name_by_id(self.fleetmanager, ship_model)

        embed = discord.Embed(title="Ship Registered", description="", color=0x03336D)
        embed.add_field(name="Name", value=" ".join([hull_number.upper(), name]))
        embed.add_field(name="Class", value=ship_model_name)
        embed.add_field(name="Registered to", value=registered_to.display_name)
        embed.add_field(name="Shipyard", value=shipyard_name)

        embed.set_thumbnail(url=registered_to.display_avatar.url)

        self.fleetmanager.register_ship(
            {
                'name': name,
                'model_id': ship_model,
                'shipyard_id': shipyard,
                'registered_to': registered_to.id,
                'status': "Rearming",
                'location': shipyard_name,
            }
        )
        return embed


    @forceregister.autocomplete("shipyard")
    @register.autocomplete("shipyard")
    async def autocomplete_shipyard(self, interaction: Interaction, current: str) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=i["name"], value=str(i["id"]))
            for i in self.fleetmanager.cached_shipyards if current.lower() in i["name"].lower()
        ]



    @forceregister.autocomplete("ship_model")
    @register.autocomplete("ship_model")
    async def autocomplete_ship_model(self, interaction: Interaction, current: str) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=i["name"], value=str(i["id"]))
            for i in self.fleetmanager.cached_ship_models if current.lower() in i["name"].lower()
        ]


async def setup(fleetmanager):
    await fleetmanager.add_cog(RegisterCog(fleetmanager))


