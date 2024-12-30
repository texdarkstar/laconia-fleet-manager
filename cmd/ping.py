import discord
from discord import Interaction
from discord.ext import commands


class PingCog(commands.Cog):
    def __init__(self, fleetmanager):
        self.fleetmanager = fleetmanager


    @commands.hybrid_command(name="ping", with_app_command=True)
    async def ping(self, ctx: Interaction):
        await ctx.send("Pong", ephemeral=True)

