import discord
from discord import Interaction, app_commands
from discord.ext import commands



class PingCog(commands.Cog, name="cogs.ping"):
    def __init__(self, fleetmanager):
        self.fleetmanager = fleetmanager


    @app_commands.command(name="ping")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message("pong", ephemeral=True)
        # raise NotImplementedError("Ping command not implemented.")


async def setup(fleetmanager):
    await fleetmanager.add_cog(PingCog(fleetmanager))

