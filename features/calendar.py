from discord.ext import commands
from datetime import datetime, timedelta, date
from dateutil.easter import easter
import discord
import asyncio

CHANNEL_ID = 1117869477669916803

class ChristianCalendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.task = self.bot.loop.create_task(self.check_date())

    def cog_unload(self):
        self.task.cancel()

    async def check_date(self):
        await self.announce_date()  # Immediately announce the date after bot starts

        while True:
            now = datetime.now()
            next_time = now.replace(hour=8, minute=0, second=0)
            if now.hour >= 8:
                next_time += timedelta(days=1)
            to_wait = (next_time - now).seconds
            await asyncio.sleep(to_wait)
            await self.announce_date()

    async def announce_date(self, test_date=None):  # Change the default value of test_date to None
        if test_date:
            today = test_date
        else:
            today = datetime.now().date()

        # The rest of the calculations should be done irrespective of whether test_date is given or not
        # So, move them outside the conditional block

        # Calculate the dates of the movable feasts for this year
        easter_date = easter(today.year)
        ash_wednesday_date = easter_date - timedelta(days=46)
        palm_sunday_date = easter_date - timedelta(days=7)
        good_friday_date = easter_date - timedelta(days=2)
        ascension_date = easter_date + timedelta(days=39)
        pentecost_date = easter_date + timedelta(days=49)
        corpus_christi_date = easter_date + timedelta(days=60)

        # Define fixed holidays
        fixed_holidays = {
            (1, 6): "Epiphany - Celebrates the revelation of God incarnate as Jesus Christ.",
            (2, 2): "Candlemas - Feast of the Presentation of Jesus Christ and Feast of the Purification of the Blessed Virgin Mary.",
            (2, 14): "St. Valentine's Day - An observance of love and affection.",
            (3, 25): "Annunciation - Celebrates the visit of the Archangel Gabriel to the Virgin Mary, during which she agreed to become the Mother of Jesus.",
            (6, 26): "Assumption of Mary - Observes the bodily taking up of the Virgin Mary into Heaven at the end of her earthly life.",
            (10, 4): "St. Francis Day - Honors St. Francis of Assisi, the patron saint of animals and the environment.",
            (10, 31): "All Hallows Eve - The day before All Saints' Day, often celebrating the lives of saints and deceased loved ones.",
            (11, 1): "All Saints' Day - Honors all saints and martyrs, both known and unknown.",
            (11, 2): "All Souls' Day - Commemorates all faithful Christians who have died but not yet reached heaven.",
            (12, 25): "Christmas - Celebrating the birth of Jesus Christ, the son of God.",
            (12, 26): "St. Stephen's Day - Honors St. Stephen, the first Christian martyr."
        }

        # Check if today is any of the movable feast dates and send the appropriate message
        if today == easter_date:
            await self.bot.get_channel(CHANNEL_ID).send(":star2: **TODAY IS A SPECIAL DAY** :star2:\nToday is Easter - Celebrating the resurrection of Jesus Christ from the dead.")
        elif today == good_friday_date:
            await self.bot.get_channel(CHANNEL_ID).send(":star2: **TODAY IS A SPECIAL DAY** :star2:\nToday is Good Friday - Commemorating the crucifixion of Jesus Christ and his death at Calvary.")
        elif today == palm_sunday_date:
            await self.bot.get_channel(CHANNEL_ID).send(":star2: **TODAY IS A SPECIAL DAY** :star2:\nToday is Palm Sunday - Commemorates Jesus's triumphant entry into Jerusalem.")
        elif today == ash_wednesday_date:
            await self.bot.get_channel(CHANNEL_ID).send(":star2: **TODAY IS A SPECIAL DAY** :star2:\nToday is Ash Wednesday - Marks the start of the Lenten period of fasting and penance.")
        elif today == ascension_date:
            await self.bot.get_channel(CHANNEL_ID).send(":star2: **TODAY IS A SPECIAL DAY** :star2:\nToday is Ascension Day - Celebrates the Ascension of Jesus Christ into heaven.")
        elif today == pentecost_date:
            await self.bot.get_channel(CHANNEL_ID).send(":star2: **TODAY IS A SPECIAL DAY** :star2:\nToday is Pentecost - Celebrates the descent of the Holy Spirit upon the Apostles and other followers of Jesus.")
        elif today == corpus_christi_date:
            await self.bot.get_channel(CHANNEL_ID).send(":star2: **TODAY IS A SPECIAL DAY** :star2:\nToday is Corpus Christi - Solemn commemoration of the institution of the Eucharist.")
        elif (today.month, today.day) in fixed_holidays:
            # If today's date matches a key in the fixed_holidays dictionary, send that message
            await self.bot.get_channel(CHANNEL_ID).send(f":star2: **TODAY IS A SPECIAL DAY** :star2:\nToday is {fixed_holidays[(today.month, today.day)]}")

