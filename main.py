import asyncio
import discord
from discord import app_commands, ui, Interaction, Member
from typing import Literal
from supabase import create_client, Client
from secret import *
from views import *



class FleetManager(discord.Client):
    def __init__(self, intents=discord.Intents):
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.guild_list = {}

        self.db = create_client(POSGRES_URL, POSGRES_KEY)
        self.ship_models = {}
        self.shipyards = {}
        self.user_ids = {}


        # asyncio.run(update_user_ids())

        self.update_shipyards()
        self.update_ship_models()


    async def update_user_ids(self):
        for i in self.user_ids.keys():
            if not self.user_ids[i]:
                name = await self.fetch_user(i)
                try:
                    self.user_ids[i] = name.display_name
                except AttributeError:
                    self.user_ids[i] = None


    def update_ship_models(self):
        resp = self.db.table("ship_models").select("name, classification").execute()
        for row in resp.data:
            self.ship_models[row['name']] = row['classification']


    def update_shipyards(self):
        resp = self.db.table("shipyards").select("name, owner").execute()
        for row in resp.data:
            self.shipyards[row['name']] = row['owner']


    async def setup_hook(self):
        for guild in GUILDS:
            g = discord.Object(id=guild)
            self.tree.copy_global_to(guild=g)
            await self.tree.sync(guild=g)

            self.guild_list[g] = guild

            for shipyard in self.shipyards.keys():
                self.user_ids[self.shipyards[shipyard]] = None

            await self.update_user_ids()


duarte = FleetManager(intents=discord.Intents.default())


@duarte.tree.command()
async def ping(interaction: Interaction):
    await interaction.response.send_message("Pong", ephemeral=True)


@duarte.tree.command()
async def testshipyards(interaction: Interaction):
    view = ShipyardView(fleetmanager=duarte)
    await interaction.response.send_message(view=view, ephemeral=DEBUG)
    await view.wait()



@duarte.tree.command()
async def register(interaction: Interaction, name: str, registered_to: Member):
    view = ClassView(name=name, fleetmanager=duarte)
    await interaction.response.send_message(view=view, ephemeral=DEBUG)
    await view.wait()


    ship_model = view.children[0].values[0]
    hull_number = new_hull(ship_model)

    embed = discord.Embed(title="Ship Registered", description="", color=0x03336D)
    embed.add_field(name="Name", value=" ".join([hull_number.upper(), name]))
    embed.add_field(name="Class", value=ship_model)
    embed.add_field(name="Registered to", value=registered_to.display_name)
    embed.set_thumbnail(url=registered_to.display_avatar.url)

    await interaction.followup.send(embed=embed, ephemeral=DEBUG)


def new_hull(model):
    model_id = 1

    ships = duarte.db.table("ships").select("*").eq("model_id", model_id).execute().data

    n = str(len(ships))
    if int(n) < 10:
        n = "0" + n

    return duarte.ship_models[model] + "-" + (n)



if __name__ == "__main__":
    duarte.run(TOKEN)
