from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def flowee(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid flowee command passed... Send **!flowee help** and I help you!")

    @flowee.command()
    async def help(self, ctx):
        help_message = """
        **Hello!**
        I am :cherry_blossom: *Flowee* :cherry_blossom: A little bot helper for everyone who wants to direct their heart towards God  :pray:

        Here's what I can do:

        :book: **Daily Verses**: I send verses every day.
        :book: **Verse for Prompt**: I send a verse for prompt when you command me with `!verse`.

        :pray: **Prayers**: I generate a prayer for you, based on the category you want to pray about. Command me with `!prayer` followed by your chosen category.
        \t:sparkles: Categories include:
        \t\t efisio, morning, healing, strength, family, forgiveness, thankfulness, protection, guidance, peace,
        \t\t gratitude, wisdom, love, patience, courage, comfort, faith, joy, hope, serenity, purity.
        \t:bulb: Example: `!prayer guidance`.

        :dove: **Prayer List**: You can join or leave the prayer list. When you are in the prayer list, your username will be included in our daily prayers.
        \t To join the prayer list, use the command `!join prayer list`.
        \t To leave the prayer list, use the command `!leave prayer list`.

        :earth_africa: **Additional Resources**: If you are looking for resources for your Walk in Christ, command me with `!resources`, and I will print them for you!  :white_heart:

        :trophy: **Bible Trivia Games**: I orchestrate Bible Trivia games! To start a game, just type `!trivia` followed by the level (1, 2, or 3) and the players' @usernames. 
        \t:bulb: Example: `!trivia 1 @user1 @user2`. Even one player alone can attend! Simply write the command to start the game and follow the instructions.
        \t:grey_exclamation: Please note that you can only start a Bible Trivia game in a dedicated channel!
        """

        await ctx.send(help_message)
