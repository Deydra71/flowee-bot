import discord
import yaml
from discord.ext import commands
from datetime import datetime, timedelta, date
from features.daily_verse import DailyVerses
from features.prayer import Prayer
from features.trivia import Trivia
from features.help import Help
from features.resources import Resources
from features.prayer_list import PrayerList
from features.calendar import ChristianCalendar
from bot_token.bot_token import token

value = 17998329146480
intents = discord.Intents.all()

with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

for flag, bit in intents.VALID_FLAGS.items():
    if value & (1 << bit):
        setattr(intents, flag, True)

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == "Hello":
        await message.channel.send("Hello")

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="!flowee help"))
    await bot.add_cog(DailyVerses(bot, config)) 
    await bot.add_cog(Prayer(bot, config))
    await bot.add_cog(Trivia(bot, config))
    bot.remove_command('help')
    await bot.add_cog(Help(bot))
    bot.add_cog(PrayerList(bot, config))
    await bot.add_cog(ChristianCalendar(bot))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Command not found: **{ctx.message.content}**. Please use a valid command.")
    else:
        raise error
    
    # # Test all announcements for the entire year
    # calendar_cog = bot.get_cog("ChristianCalendar")
    # current_year = datetime.now().year

    # for month in range(1, 13):  # Loop through all months
    #     for day in range(1, 32):  # Max number of days in a month
    #         try:
    #             await calendar_cog.announce_date(current_year, month, day)
    #         except ValueError:  # This exception will be raised for invalid dates like February 30
    #             continue

bot.run(token)
