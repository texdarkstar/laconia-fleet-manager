import asyncio
import discord
from discord import app_commands, ui, Interaction, Member, Intents
from discord.ext import commands
from typing import Literal
from supabase import create_client, Client
from secret import *
from ui import *
from cmd.ping import PingCog
from cmd.register import RegisterCog


class FakeUser(object):
    def __init__(self, user_id):
        self.id = self.display_name = user_id

    def __str__(self):
        return str(self.id)


class FleetManager(commands.Bot):
    def __init__(self, intents=Intents, *args, **kwargs):
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        self.command_prefix = "|"

        super().__init__(intents=intents, *args, **kwargs)
        # self.tree = app_commands.CommandTree(self)
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
        for member in self.users:
            self.user_ids[member.id] = member


    def return_user(self, user_id: int):
        for user in self.get_all_members():
            # print(f"{user.display_name}({user.id}) == {user_id}")

            if int(user.id) == int(user_id):
                return user

        return FakeUser(user_id)


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
        await self.add_cog(PingCog(self))
        await self.add_cog(RegisterCog(self))


        for guild in GUILDS:
            g = discord.Object(id=guild)
            self.tree.copy_global_to(guild=g)
            await self.tree.sync(guild=g)

            self.guild_list[g] = guild

    def register_ship(self, shipdata: dict):
        self.db.table("ships").insert(shipdata).execute()



duarte = FleetManager(intents=Intents.default(), command_prefix="|")



@duarte.tree.command()
async def queryships(interaction: Interaction, member: Member):

    resp1 = duarte.db.table("ships").select("*").eq("registered_to", member.id).execute()
    resp2 = duarte.db.table("ship_models").select("*").execute()
    models = {}

    for row in resp2.data:
        models[row["id"]] = row["name"]

    embed = discord.Embed(title=f"Registered Ships for {member.display_name}", color=0x03336D)

    ship_names = []
    ship_statuses = []
    ship_classes = []

    for row in resp1.data:
        model = models[row["model_id"]]
        hull_number = get_hull_number(row["id"])

        ship_names.append(hull_number + " " + row["name"])
        ship_statuses.append(row["status"])
        ship_classes.append(model)


    embed.add_field(name="Name", value="\n".join(ship_names))
    embed.add_field(name="Class", value="\n".join(ship_classes))
    embed.add_field(name="Status", value="\n".join(ship_statuses))

    await interaction.response.send_message(embed=embed, ephemeral=DEBUG)

#
# @duarte.tree.command()
# async def ping(interaction: Interaction):
#     await interaction.response.send_message("Pong", ephemeral=True)


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

    await interaction.response.send_message("Database reloaded!", ephemeral=True)


# @duarte.tree.command()
# async def register(interaction: Interaction, name: str, registered_to: Member):
#     # view = ModelView(fleetmanager=duarte)
#     view = RegisterView(fleetmanager=duarte)
#     await interaction.response.send_message(view=view, ephemeral=True)
#     await view.wait()
#
#     await interaction.delete_original_response()
#
#
#     ship_model = view.children[0].values[0]
#     shipyard = view.children[1].values[0]
#
#     hull_number = new_hull(ship_model)
#
#     embed = discord.Embed(title="Ship Registered", description="", color=0x03336D)
#     embed.add_field(name="Name", value=" ".join([hull_number.upper(), name]))
#     embed.add_field(name="Class", value=ship_model)
#     embed.add_field(name="Registered to", value=registered_to.display_name)
#     embed.add_field(name="Shipyard", value=shipyard)
#
#     embed.set_thumbnail(url=registered_to.display_avatar.url)
#
#     await interaction.followup.send(embed=embed)
#     duarte.register_ship(
#         {
#             'name': name,
#             'model_id': get_model_id_by_name(ship_model),
#             'shipyard_id': get_shipyard_id(shipyard),
#             'registered_to': registered_to.id,
#             'status': "Rearming",
#             'location': shipyard + " shipyards"
#         }
#     )


def get_model_id_by_name(model):
    return duarte.ship_models[model]['id']


def get_shipyard_id(shipyard):
    return duarte.shipyards[shipyard]['id']


def get_hull_number(ship_id: int):
    # get a list of all ships of a model matching our ships model
    # for every instance of the constructed ship of the same model, incrememnt our hull number

    ship_list = duarte.db.table("ships").select("*").execute().data

    models = {}
    same_models = []

    for row in duarte.db.table("ship_models").select("*").execute().data:
        models[row["id"]] = row["classification"]

    ship = duarte.db.table("ships").select("*").eq("id", ship_id).execute().data.pop()  # should only be 1 result

    for row in ship_list:
        if row["model_id"] == ship["model_id"]:
            same_models.append(row["id"])

    n = str(same_models.index(ship["id"]) + 1)

    if int(n) < 10:
        n = "0" + n

    hull_string = models[ship["model_id"]] + "-" + n


    return hull_string


def new_hull(model):
    model_id = get_model_id_by_name(model)
    hull_number = duarte.ship_models[model]['classification']

    ships = duarte.db.table("ships").select("*").eq("model_id", model_id).execute().data

    n = str(len(ships) + 1)

    if int(n) < 10:
        n = "0" + n

    hull_number += "-" + n

    return hull_number



if __name__ == "__main__":
    duarte.run(TOKEN)
