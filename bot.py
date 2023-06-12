import discord
from discord.ext import commands

# Create instance of bot
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

bot.run('bot-token')
