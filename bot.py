import discord
from discord.ext import commands
from features.daily_verse import DailyVerses
from features.prayer import Prayer
from features.trivia import Trivia
from features.help import Help
from features.resources import Resources
from features.prayer_list import PrayerList
from bot_token.bot_token import token

value = 17998329146480
intents = discord.Intents.all()

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
    await bot.add_cog(DailyVerses(bot)) 
    await bot.add_cog(Prayer(bot))
    await bot.add_cog(Trivia(bot))
    bot.remove_command('help')
    await bot.add_cog(Help(bot))
    await bot.add_cog(Resources(bot))
    await bot.add_cog(PrayerList(bot))


bot.run(token)
