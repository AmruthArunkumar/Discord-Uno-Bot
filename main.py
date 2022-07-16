from deck import Deck
import discord
from discord import app_commands

DISCORD_TOKEN = "OTk2NzAzMDY4MjQ0Njc2Njk4.G9VA3k.Xh8uF5Utfx4ahyX-gefdNYlXCgd6G93u37T14c"

class client(discord.Client):
    async def startup(self):
        await self.wait_until_ready()
        await tree.sync(guild = discord.Object(id = 996703969168605255))

bot = client()
tree = app_commands.CommandTree(bot)

@bot.event
async def on_started():
    serverCount = 0
    for server in bot.guilds:
        print(str(server.id) + ": " + str(server.name))
        serverCount += 1
    print("Bot in " + str(serverCount) + " servers")

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@bot.command(
    guild = discord.Object(id = 996703969168605255),
    name = "setup",
    description = "sets up the game"
)
async def setup(ctx: discord.Interaction):
    deck = Deck()
    await ctx.response.send_message("Setup Complete :D")

@bot.command(
    guild = discord.Object(id = 996703969168605255),
    name = "hello",
    description = "responds to msg"
)
async def hello(ctx: discord.Interaction):
    await ctx.response.send_message("hi")

@bot.command(
    guild = discord.Object(id = 996703969168605255),
    name = "private",
    description = "responds privately"
)
async def private(ctx: discord.Interaction):
    await ctx.response.send_message("hi", ephemeral = True)

@bot.command(
    guild = discord.Object(id = 996703969168605255),
    name = "delete",
    description = "deletes the msg"
)
async def delete(ctx: discord.Interaction):
    response = await ctx.respond("hi")
    await response.delete()
    await ctx.message.delete()

bot.run(DISCORD_TOKEN)
