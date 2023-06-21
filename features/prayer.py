import json
import discord
from discord.ext import commands
import random

# Possible categories: Efisio, healing, family, strength, protection, morning, forgiveness, thankfulness, guidance, peace, gratitude, wisdom, hope, purity, serenity, joy, faith, courage, patience, love
class Prayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('files/prayers.json', 'r', encoding='utf-8') as f:
            self.prayers = json.load(f)
        self.prayers_left = {prayer['prayer_name'].split('_')[0]: [] for prayer in self.prayers}
    
    @commands.command()
    async def prayer(self, ctx, prayer_name=None):
        if prayer_name is None:
            await ctx.send("Please specify the name of a prayer, like so: `!prayer morning`.")
            return
        else:
            prayer_name = prayer_name.lower()
            if not self.prayers_left[prayer_name]:
                self.prayers_left[prayer_name] = [prayer for prayer in self.prayers if prayer['prayer_name'].startswith(prayer_name)]
            prayer = random.choice(self.prayers_left[prayer_name])
            self.prayers_left[prayer_name].remove(prayer)

        if prayer is None:
            await ctx.send(f"There's no prayer with the name {prayer_name}. Please check the spelling and try again.")
        else:
            await ctx.send(f"Here's your prayer, {ctx.message.author.mention}! God bless you! :pray:\n\n*{prayer['prayer_content']}*")
