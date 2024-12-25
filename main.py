import discord
# import ship_classes
from discord import app_commands, ui, Interaction
from typing import Literal
from supabase import create_client, Client
from secret import *
from classview import *


class FleetManager(discord.Client):
    def __init__(self, intents=discord.Intents):
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.guild_list = {}

        self.db = create_client(POSGRES_URL, POSGRES_KEY)
        self.ship_models = {}

        resp = self.db.table("ship_models").select("name, classification").execute()
        for row in resp.data:
            self.ship_models[row['name']] = row['classification']


    async def setup_hook(self):
        for guild in GUILDS:
            g = discord.Object(id=guild)
            self.tree.copy_global_to(guild=g)
            await self.tree.sync(guild=g)

            self.guild_list[g] = guild



duarte = FleetManager(intents=discord.Intents.default())


@duarte.tree.command()
async def ping(interaction: Interaction):
    await interaction.response.send_message("Pong", ephemeral=True)


@duarte.tree.command()
async def testshipyards(interaction: Interaction, shipyard: Literal["Roberta", "Helicon", "Terrapin"]):
    await interaction.response.send_message(f"Shipyard: {shipyard}", ephemeral=True)


@duarte.tree.command()
async def register(interaction: Interaction, name: str, registered_to: str):
    view = ClassView(name=name, fleetmanager=duarte)
    await interaction.response.send_message(view=view, ephemeral=DEBUG)
    await view.wait()


    ship_model = view.children[0].values[0]
    embed = discord.Embed(title="Ship Registered!", description="", color=0x03336D)
    embed.add_field(name="Name", value=name)
    embed.add_field(name="Class", value=ship_model)

    await interaction.followup.send(embed=embed, ephemeral=DEBUG)


if __name__ == "__main__":
    duarte.run(TOKEN)
