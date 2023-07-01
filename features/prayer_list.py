import discord
from discord.ext import commands, tasks
import json
import asyncio
import os
from datetime import datetime, timedelta
import random

PRAYER_CHANNEL_ID = 1121786563995631666
PRAYER_LIST_FILE = 'files/prayer_list.json' 
PRAYER_TEXT_FILE = 'files/prayers_list.json'

class PrayerList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_prayer_list()
        self.load_prayer_text()
        self.send_prayer.start()

    def cog_unload(self):
        self.send_prayer.cancel()

    def load_prayer_list(self):
        if os.path.exists(PRAYER_LIST_FILE):
            with open(PRAYER_LIST_FILE, 'r') as f:
                data = f.read().strip()
                if data:
                    self.prayer_list = json.loads(data)
                    self.prayer_list = [self.bot.get_user(user_id) for user_id in self.prayer_list]
                else:
                    self.prayer_list = []
        else:
            self.prayer_list = []

    def save_prayer_list(self):
        with open(PRAYER_LIST_FILE, 'w') as f:
            json.dump([user.id for user in self.prayer_list], f)

    def load_prayer_text(self):
        if os.path.exists(PRAYER_TEXT_FILE):
            with open(PRAYER_TEXT_FILE, 'r') as f:
                self.prayer_text = json.load(f)['prayers']
        self.unused_prayers = self.prayer_text.copy()

    def get_prayer(self):
        if not self.unused_prayers:
            self.unused_prayers = self.prayer_text.copy()
        prayer_for_today = random.choice(self.unused_prayers)
        self.unused_prayers.remove(prayer_for_today)
        return prayer_for_today

    @commands.command()
    async def join_prayer_list(self, ctx):
        if ctx.author not in self.prayer_list:
            self.prayer_list.append(ctx.author)
            self.save_prayer_list()
            await ctx.send(f"{ctx.author.mention} has been added to the prayer list.")
        else:
            await ctx.send(f"{ctx.author.mention}, you're already in the prayer list.")

    @commands.command()
    async def leave_prayer_list(self, ctx):
        if ctx.author in self.prayer_list:
            self.prayer_list.remove(ctx.author)
            self.save_prayer_list()
            await ctx.send(f"{ctx.author.mention} has been removed from the prayer list.")
        else:
            await ctx.send(f"{ctx.author.mention}, you're not in the prayer list.")

    @tasks.loop(hours=24)
    async def send_prayer(self):
        prayer_channel = self.bot.get_channel(PRAYER_CHANNEL_ID)
        prayer_for_today = self.get_prayer()
        if not self.prayer_list:
            await prayer_channel.send("There's currently no one on the prayer list. Let's all take a moment to send some positive thoughts and prayers for everyone in our community :pray: :heart:")
        else:
            prayer = """:dove: **Prayer of the Day** :dove: \n\n"""
            prayer += f"*{prayer_for_today}*\n\n"
            prayer += "\n".join(member.mention for member in self.prayer_list)
            prayer += "\n\n*In Jesus' name, we pray. Amen.*"
            await prayer_channel.send(prayer)

    @send_prayer.before_loop
    async def before_send_prayer(self):
        now = datetime.now()
        future = datetime.now().replace(hour=10)
        if now.hour >= 10:   # if it's past 8 AM, schedule for next day
            future += timedelta(days=1)
        await discord.utils.sleep_until(future)  # wait until the specified time
