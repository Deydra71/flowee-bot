import discord
from discord.ext import commands, tasks
import random
import aiohttp

class DailyVerses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_daily_verse.start()

    @tasks.loop(hours=24)
    async def send_daily_verse(self):
        # code to fetch and send the daily verse

    @send_daily_verse.before_loop
    async def before_send_daily_verse(self):
        # code to wait until the time is 8 AM CET

    @commands.command(name='verse')
    async def send_verse(self, ctx):
        # code to fetch and send a verse on demand
