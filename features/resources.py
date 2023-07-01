from discord.ext import commands

class Resources(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def resources(self, ctx):
        resources_message = """
:star: **Helpful Christian Resources** :star: \n
Here are some resources that might help you in your spiritual journey :cloud_tornado:
1. :vibration_mode: **YouVersion Bible App** (https://www.youversion.com/): A widely-used Bible application with multiple translations, reading plans, and more.
2. :computer: **Bible Gateway** (https://www.biblegateway.com/): An online searchable Bible in more than 200 versions and 70 languages.
3. :newspaper: **Christianity Today** (https://www.christianitytoday.com/): A popular Christian magazine that features articles on various topics related to Christian faith and life.
4. :book: **Desiring God** (https://www.desiringgod.org/): A resource library of sermons, articles, books, and more from John Piper and other contributors.
5. :cross: **Crosswalk** (https://www.crosswalk.com/): Christian news, devotional, and Bible study resources.
6. :family: **Focus on the Family** (https://www.focusonthefamily.com/): A global Christian ministry dedicated to helping families thrive.
"""

        await ctx.send(resources_message)
