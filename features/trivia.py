import discord
from discord.ext import commands, tasks
import random
import json
import asyncio

TRIVIA_CHANNEL_ID = 1120358578256093385 # Please replace with your designated channel ID

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scores = {}
        self.players = []
        self.correct_messages = []

    async def print_scores(self, ctx):
        message = 'Trivia game ended! Here are the scores:\n'
        sorted_scores = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        for player, score in sorted_scores:
            message += f'{player.mention}: {score}\n'
        if sorted_scores:
            winners = [player for player, score in sorted_scores if score == sorted_scores[0][1]]
            if len(winners) == 1:
                message += f':trophy: Congratulations {winners[0].mention}! You won! :trophy:'
            else:
                message += ':trophy: Congratulations ' + ', '.join(player.mention for player in winners) + '! You all tied for first place! :trophy:'
        else:
            message += ':four_leaf_clover: No one got any points. Better luck next time! :four_leaf_clover:'
        await ctx.send(message)

    def check_answer(self, answers):
        def check(m):
            if m.channel.id == self.channel.id and m.author in self.players and m.content.lower() in answers:
                return True
            return False
        return check

    @commands.command()
    async def trivia(self, ctx, level: int, *members: discord.Member):
        if not ctx.message.channel.id == TRIVIA_CHANNEL_ID:
            await ctx.send('Please use the trivia channel to start a trivia game!')
            return
        self.players = list(members)
        self.channel = ctx.channel
        self.scores = {member: 0 for member in members}
        players_mention = ', '.join(member.mention for member in self.players)
        await ctx.send(f'The players are: {players_mention}.')
        await asyncio.sleep(2)
        await ctx.send('Starting trivia game in 5 seconds...')
        await asyncio.sleep(5)

        with open(f'files/questions{level}.json', 'r') as f:
            questions = json.load(f)
        questions = {k: [x.lower() for x in v] for k, v in questions.items()}
        i = 0
        for question, answers in random.sample(list(questions.items()), 7):
            await ctx.send(f'Question {i+1}: {question}')
            try:
                response = await self.bot.wait_for('message', check=self.check_answer(answers), timeout=20)
                await response.delete()
                if response.content.lower() in answers:
                    self.scores[response.author] += 1
                    await ctx.send(f'{response.author.mention} got it right!')
            except asyncio.TimeoutError:
                await ctx.send('Time\'s up!')
            await ctx.send(f'The correct answer(s) is/are: {", ".join(answers)}')
            i += 1
        await self.print_scores(ctx)
