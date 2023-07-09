import discord
from discord.ext import commands, tasks
import json
import random
from datetime import datetime, timedelta

class DailyVerses(commands.Cog):

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.load_verses()
        self.send_daily_verse.start()

    def load_verses(self):
        try:
            with open(self.config['verses'], 'r', encoding='utf-8-sig') as f:
                self.books = json.load(f)
        except FileNotFoundError:
            print('File not found')
        except json.JSONDecodeError:
            print('Could not decode JSON')

    def pick_random_verse(self):
        book = random.choice(self.books)
        chapter_number = random.choice(range(len(book['chapters'])))
        chapter = book['chapters'][chapter_number]
        verse = random.choice(chapter)
        return f"{book['name']} {chapter_number+1}:{chapter.index(verse)+1}\n\n*{verse}*"

    @commands.command()
    async def verse(self, ctx):
        verse = self.pick_random_verse()
        await ctx.send(verse)

    @tasks.loop(hours=24)  # loop every 24 hours
    async def send_daily_verse(self):
        channel = self.bot.get_channel(1117869477669916803)
        verse = self.pick_random_verse()
        await channel.send(f":raised_hands: **VERSE OF THE DAY** :raised_hands:\n\n{verse}")

    @send_daily_verse.before_loop
    async def before_send_daily_verse(self):
        now = datetime.now()
        future = datetime.now().replace(hour=8)
        if now.hour >= 11:   # if it's past 11 AM, schedule for next day
            future += timedelta(days=1)
        await discord.utils.sleep_until(future)
