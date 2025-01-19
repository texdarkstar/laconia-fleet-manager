import discord
from discord import Interaction, app_commands
from discord.ext import commands
from utils import *
from settings import DEBUG
from time import sleep


class ShipsCog(commands.Cog, name="cogs.ships"):
    def __init__(self, fleetmanager):
        self.fleetmanager = fleetmanager


    @app_commands.command(name="ships")
    async def ships(self, interaction: Interaction, member: discord.User):
        async with interaction.channel.typing():
            await interaction.response.defer()

            resp1 = self.fleetmanager.db.table("ships").select("*").eq("registered_to", member.id).neq("status", "Destroyed").execute()
            resp2 = self.fleetmanager.db.table("ship_models").select("*").execute()
            models = {}

            for row in resp2.data:
                models[row["id"]] = row["name"]

            embed = discord.Embed(title=f"Registered Ships for {member.display_name}", color=0x03336D)
            embed.set_thumbnail(url=member.display_avatar.url)

            buffer = sorted(resp1.data, key=lambda x: x["id"], reverse=True)
            embeds = []
            num_fields = 0

            while buffer:
                data = buffer.pop()
                model = models[data["model_id"]]
                hull_number = get_hull_number(self.fleetmanager, data["id"])
                full_name = f"{hull_number} {data['name']}"

                if len(full_name) > 40:
                    full_name = full_name[:40] + "..."

                print(full_name)
                row = f"> Name: {full_name}\n> Class: {model}\n> Status: {data['status']}"

                if (len(embed) >= 6000) or (num_fields == 25):
                    embeds.append(embed)
                    embed = discord.Embed(color=0x03336D)
                    print("New embed created")
                    num_fields = 0

                embed.add_field(name="", value=row, inline=False)
                num_fields += 1

            embeds.append(embed)

            for e in embeds:
                await interaction.followup.send(embed=e)
                sleep(.2)


async def setup(fleetmanager):
    await fleetmanager.add_cog(ShipsCog(fleetmanager))

