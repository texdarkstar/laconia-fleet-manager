import discord
import ship_classes
from discord import app_commands, ui
from secret import *
from classview import *


class FleetManager(discord.Client):
    def __init__(self, intents=discord.Intents):
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.guild_list = {}


    async def setup_hook(self):
        for guild in GUILDS:
            g = discord.Object(id=guild)
            self.tree.copy_global_to(guild=g)
            await self.tree.sync(guild=g)

            self.guild_list[g] = guild



duarte = FleetManager(intents=discord.Intents.default())


@duarte.tree.command()
async def ping(ctx):
    await ctx.response.send_message("Pong", ephemeral=True)


@duarte.tree.command()
async def register(ctx, shipname: str):
    view = ClassView(shipname=shipname)
    await ctx.response.send_message(view=view, ephemeral=DEBUG)
    await view.wait()


    shipclass = view.children[0].values[0]
    embed = discord.Embed(title="Ship Registered!", description="", color=0x03336D)
    embed.add_field(name="Name", value=shipname)
    embed.add_field(name="Class", value=shipclass)

    await ctx.followup.send(embed=embed, ephemeral=DEBUG)


if __name__ == "__main__":
    duarte.run(TOKEN)
