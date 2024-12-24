import discord
from discord import app_commands
from secret import TOKEN

bot_id = "Laconia Fleet Manager"

GUILDS = [
    discord.Object(id=1290894138547376238)  # Tex's Bot Stuff
    ]


class FleetManager(discord.Client):
    def __init__(self, intents=discord.Intents):
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)


    async def setup_hook(self):
        for guild in GUILDS:

            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)



duarte = FleetManager(intents=discord.Intents.default())


@duarte.tree.command()
async def ping(ctx):
    await ctx.response.send_message("Pong")



if __name__ == "__main__":

    duarte.run(TOKEN)
