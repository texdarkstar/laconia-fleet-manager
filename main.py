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
from sys import stderr
from os.path import exists
import logging


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
        self.logger = logging.getLogger(__name__)
        n = 1
        logfile = f"duarte_{n}.log"

        while exists(f"duarte_{n}.log"):
            n += 1

        logging.basicConfig(filename=logfile, level=logging.INFO)

        # self.logger.addHandler(logging.StreamHandler(stderr))
        self.logger.info("Starting up")

        self.command_prefix = "|"

        super().__init__(intents=intents, *args, **kwargs)
        # self.tree = app_commands.CommandTree(self)
        self.guild_list = {}

        self.db = create_client(POSGRES_URL, POSGRES_KEY)

        self.ship_models = {}
        self.user_ids = {}
        # self.cached_ships = []
        # self.cached_ship_models = []
        # self.cached_shipyards = []
        self.cached_tables = {}
        self.update_cache()


    def update_cache(self):
        self.cached_tables["ships"] = self.db.table("ships").select("*").execute().data
        self.cached_tables["ship_models"] = self.db.table("ship_models").select("*").execute().data
        self.cached_tables["shipyards"] = self.db.table("shipyards").select("*").execute().data

        self.logger.info("Cache updated")


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

    @commands.after_invoke
    async def at_after_invoke(self, ctx):
        self.update_cache()

    def register_ship(self, shipdata: dict):
        self.db.table("ships").insert(shipdata).execute()


    def update_status(self, ship_id: int, status: str):
        self.db.table("ships").update({"status": status}).eq("id", ship_id).execute()


duarte = FleetManager(intents=Intents.default(), command_prefix="|")


@duarte.tree.command()
async def reload(interaction: Interaction):
    if not is_officer(interaction.user):
        duarte.logger.info(f"User {interaction.user} tried to use /reload")
        await interaction.response.send_message("You are not authorized to use this command", ephemeral=True)
        return

    cogs = []
    for cog in duarte.cogs.values():
        cogs.append(cog.qualified_name)

    for cog in cogs:
        await duarte.reload_extension(cog)

    await interaction.response.send_message("Reloaded", ephemeral=True)

    duarte.update_cache()
    await duarte.sync_commands()


if __name__ == "__main__":
    duarte.run(TOKEN)
