import asyncio
import discord
from discord import app_commands, ui, Interaction, Member
# from typing import Literal
from supabase import create_client, Client
from secret import *
from ui import *



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
        self.ships = {}

        self.update_shipyards()
        self.update_ship_models()
        self.update_ships()


    async def update_user_ids(self):
        for i in self.user_ids.keys():
            if not self.user_ids[i]:
                name = await self.fetch_user(i)
                try:
                    self.user_ids[i] = name.display_name
                except AttributeError:
                    self.user_ids[i] = None



    def update_ships(self):
        resp = self.db.table("ships").select("*").execute()
        self.ships = resp.data
        for row in self.ships:
            self.user_ids[row["registered_to"]] = None



    def update_ship_models(self):
        resp = self.db.table("ship_models").select("*").execute()
        for row in resp.data:
            self.ship_models[row['name']] = {
                'id': row['id'],
                'designer': row['designer'],
                'classification': row['classification']
            }
            self.user_ids[row['designer']] = None



    def update_shipyards(self):
        resp = self.db.table("shipyards").select("*").execute()
        for row in resp.data:
            self.shipyards[row['name']] = {
                'id': row['id'],
                'owner': row['owner']
            }
            self.user_ids[row['owner']] = None



    async def setup_hook(self):
        for guild in GUILDS:
            g = discord.Object(id=guild)
            self.tree.copy_global_to(guild=g)
            await self.tree.sync(guild=g)

            self.guild_list[g] = guild

            await self.update_user_ids()


    def register_ship(self, shipdata: dict):
        self.db.table("ships").insert(shipdata).execute()



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
async def reload(interaction: Interaction):
    duarte.update_shipyards()
    duarte.update_ship_models()
    duarte.update_ships()

    await duarte.update_user_ids()
    await interaction.response.send_message("Database reloaded!", ephemeral=True)


@duarte.tree.command()
async def register(interaction: Interaction, name: str, registered_to: Member):
    # view = ModelView(fleetmanager=duarte)
    view = RegisterView(fleetmanager=duarte)
    await interaction.response.send_message(view=view, ephemeral=True)
    await view.wait()

    await interaction.delete_original_response()


    ship_model = view.children[0].values[0]
    shipyard = view.children[1].values[0]

    hull_number = new_hull(ship_model)

    embed = discord.Embed(title="Ship Registered", description="", color=0x03336D)
    embed.add_field(name="Name", value=" ".join([hull_number.upper(), name]))
    embed.add_field(name="Class", value=ship_model)
    embed.add_field(name="Registered to", value=registered_to.display_name)
    embed.add_field(name="Shipyard", value=shipyard)

    embed.set_thumbnail(url=registered_to.display_avatar.url)

    await interaction.followup.send(embed=embed)
    duarte.register_ship(
        {
            'name': name,
            'model_id': get_model_id(ship_model),
            'shipyard_id': get_shipyard_id(shipyard),
            'registered_to': registered_to.id,
            'status': "Rearming",
            'location': shipyard + " shipyards"
        }
    )


def get_model_id(model):
    return duarte.ship_models[model]['id']


def get_shipyard_id(shipyard):
    return duarte.shipyards[shipyard]['id']


def new_hull(model):
    model_id = get_model_id(model)
    hull_number = duarte.ship_models[model]['classification']

    ships = duarte.db.table("ships").select("*").eq("model_id", model_id).execute().data

    n = str(len(ships) + 1)
    if int(n) < 10:
        n = "0" + n

    hull_number += "-" + n

    return hull_number



if __name__ == "__main__":
    duarte.run(TOKEN)
