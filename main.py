import asyncio
import discord
from discord import app_commands, ui, Interaction, Member, Intents
from discord.ext import commands
from typing import Literal
from supabase import create_client, Client
from settings import *
from ui import *
from utils import *
from cogs.ping import PingCog
from cogs.register import RegisterCog


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
        self.user_ids = {}
        self.cached_ships = []
        self.cached_ship_models = []
        self.cached_shipyards = []

        self.update_cache()


    def update_cache(self):
        self.cached_ships = self.db.table("ships").select("*").execute().data
        self.cached_ship_models = self.db.table("ship_models").select("*").execute().data
        self.cached_shipyards = self.db.table("shipyards").select("*").execute().data


    async def update_user_ids(self):
        for member in self.users:
            self.user_ids[member.id] = member


    def return_user(self, user_id: int):
        for user in self.get_all_members():
            # print(f"{user.display_name}({user.id}) == {user_id}")

            if int(user.id) == int(user_id):
                return user

        return FakeUser(user_id)


    async def sync_commands(self):
        for guild in GUILDS:
            g = discord.Object(id=guild)
            self.tree.copy_global_to(guild=g)
            await self.tree.sync(guild=g)

            self.guild_list[g] = guild


    async def setup_hook(self):
        for cog in COGS:
            await self.load_extension(cog)

        await self.sync_commands()


    def register_ship(self, shipdata: dict):
        self.db.table("ships").insert(shipdata).execute()


    def update_status(self, ship_id: int, status: str):
        self.db.table("ships").update({"status": status}).eq("id", ship_id).execute()


duarte = FleetManager(intents=Intents.default(), command_prefix="|")


@duarte.tree.command()
async def reload(interaction: Interaction):
    if not is_officer(interaction.user):
        await interaction.response.send_message("You are not authorized to use this command", ephemeral=True)
        return

    cogs = []

    for cog in duarte.cogs.values():
        cogs.append(cog)

    for cog in cogs:
        await duarte.reload_extension(cog.qualified_name)

    await interaction.response.send_message("Cogs reloaded", ephemeral=True)
    duarte.update_cache()

    await duarte.sync_commands()


@duarte.tree.command()
async def load(interaction: Interaction, cog: str):
    if not is_officer(interaction.user):
        await interaction.response.send_message("You are not authorized to use this command", ephemeral=True)
        return

    await duarte.load_extension("cogs." + cog)
    await interaction.response.send_message(f"Loaded cog.{cog}", ephemeral=True)

    await duarte.sync_commands()


if __name__ == "__main__":
    duarte.run(TOKEN)
