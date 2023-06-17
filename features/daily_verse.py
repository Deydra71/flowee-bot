# daily_verses.py
import discord
from discord.ext import commands, tasks
import random
import aiohttp
import json

class DailyVerses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_daily_verse.start()
        self.load_verses()

    @tasks.loop(hours=24)
    async def send_daily_verse(self):
        verse = self.pick_random_verse()
        # Send the verse to the channel

    @send_daily_verse.before_loop
    async def before_send_daily_verse(self):
        # code to wait until the time is 8 AM CET

    @commands.command(name='verse')
    async def send_verse(self, ctx):
        verse = self.pick_random_verse()
        await ctx.send(verse)

    def load_verses(self):
        with open('../en_kjv.json', 'r') as f:
            self.books = json.load(f)
        self.picked_verses = set()

    def pick_random_verse(self):
        while True:
            book = random.choice(self.books)
            chapter = random.choice(book['chapters'])
            verse = random.choice(chapter)
            verse_id = f"{book['abbrev']}_{chapter.index(verse)+1}_{verse}"
            if verse_id not in self.picked_verses:
                self.picked_verses.add(verse_id)
                if len(self.picked_verses) == sum(len(chapter) for book in self.books for chapter in book['chapters']):
                    self.picked_verses.clear()  # All verses have been picked, reset
                return verse
