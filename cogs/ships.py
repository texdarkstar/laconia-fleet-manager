import discord
from discord import Interaction, app_commands
from discord.ext import commands
from utils import *
from settings import DEBUG


class ShipsCog(commands.Cog, name="cogs.ships"):
    def __init__(self, fleetmanager):
        self.fleetmanager = fleetmanager


    @app_commands.command(name="ships")
    async def ships(self, interaction: Interaction, member: discord.User):
        async with interaction.channel.typing():
            resp1 = self.fleetmanager.db.table("ships").select("*").eq("registered_to", member.id).execute()
            resp2 = self.fleetmanager.db.table("ship_models").select("*").execute()
            models = {}

            for row in resp2.data:
                models[row["id"]] = row["name"]

            embed = discord.Embed(title=f"Registered Ships for {member.display_name}", color=0x03336D)

            ship_names = []
            ship_statuses = []
            ship_classes = []

            for row in resp1.data:
                model = models[row["model_id"]]
                hull_number = get_hull_number(self.fleetmanager, row["id"])

                ship_names.append(hull_number + " " + row["name"])
                ship_statuses.append(row["status"])
                ship_classes.append(model)

            embed.add_field(name="Name", value="\n".join(ship_names))
            embed.add_field(name="Class", value="\n".join(ship_classes))
            embed.add_field(name="Status", value="\n".join(ship_statuses))

            embed.set_thumbnail(url=member.display_avatar.url)

            await interaction.response.send_message(embed=embed)


async def setup(fleetmanager):
    await fleetmanager.add_cog(ShipsCog(fleetmanager))

