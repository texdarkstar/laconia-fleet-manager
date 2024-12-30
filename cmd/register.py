import discord
from discord import Interaction, Member, Embed
from discord.ext import commands
from ui import *



class RegisterCog(commands.Cog):
    def __init__(self, fleetmanager):
        self.fleetmanager = fleetmanager

    @commands.hybrid_command(name="register", with_app_command=True)
    async def register(self, ctx: Interaction, name: str, registered_to: Member):
        # view = ModelView(fleetmanager=duarte)
        view = RegisterView(fleetmanager=self.fleetmanager)
        await ctx.response.send_message(view=view, ephemeral=True)
        await view.wait()

        await ctx.delete_original_response()

        ship_model = view.children[0].values[0]
        shipyard = view.children[1].values[0]

        hull_number = new_hull(ship_model)

        embed = discord.Embed(title="Ship Registered", description="", color=0x03336D)
        embed.add_field(name="Name", value=" ".join([hull_number.upper(), name]))
        embed.add_field(name="Class", value=ship_model)
        embed.add_field(name="Registered to", value=registered_to.display_name)
        embed.add_field(name="Shipyard", value=shipyard)

        embed.set_thumbnail(url=registered_to.display_avatar.url)

        await ctx.followup.send(embed=embed)
        self.fleetmanager.register_ship(
            {
                'name': name,
                'model_id': get_model_id_by_name(ship_model),
                'shipyard_id': get_shipyard_id(shipyard),
                'registered_to': registered_to.id,
                'status': "Rearming",
                'location': shipyard + " shipyards"
            }
        )


