from discord.ext import commands
from datetime import datetime, timedelta, date
from dateutil.easter import easter
import asyncio

CHANNEL_ID = 1155508025394745364

class ChristianCalendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.task = self.bot.loop.create_task(self.check_date())

    def cog_unload(self):
        self.task.cancel()

    async def check_date(self):
        while True:
            now = datetime.now()
            next_time = now.replace(hour=8, minute=0, second=0)
            if now.hour >= 8:
                next_time += timedelta(days=1)
            to_wait = (next_time - now).seconds
            await asyncio.sleep(to_wait)
            await self.announce_date()

    async def announce_date(self, year=None, month=None, day=None):
        if year and month and day:
            today = date(year, month, day)
        else:
            today = datetime.now().date()
        
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
            (1, 6): "*Epiphany*\n\nCelebrates the revelation of God incarnate as Jesus Christ.",
            (2, 2): "*Candlemas*\n\nFeast of the Presentation of Jesus Christ and Feast of the Purification of the Blessed Virgin Mary.",
            (2, 14): "*St. Valentine's Day*\n\nAn observance of love and affection.",
            (3, 25): "*Annunciation*\n\nCelebrates the visit of the Archangel Gabriel to the Virgin Mary, during which she agreed to become the Mother of Jesus.",
            (6, 26): "*Assumption of Mary*\n\nObserves the bodily taking up of the Virgin Mary into Heaven at the end of her earthly life.",
            (10, 4): "*St. Francis Day*\n\nHonors St. Francis of Assisi, the patron saint of animals and the environment.",
            (10, 31): "*All Hallows Eve*\n\nThe day before All Saints' Day, often celebrating the lives of saints and deceased loved ones.",
            (11, 1): "*All Saints' Day*\n\nHonors all saints and martyrs, both known and unknown.",
            (11, 2): "*All Souls' Day*\n\nCommemorates all faithful Christians who have died but not yet reached heaven.",
            (12, 25): "*Christmas*\n\nCelebrating the birth of Jesus Christ, the son of God.",
            (12, 26): "*St. Stephen's Day*\n\nHonors St. Stephen, the first Christian martyr."
        }

        # Check if today is any of the movable feast dates and send the appropriate message
        if today == easter_date:
            await self.bot.get_channel(CHANNEL_ID).send(":star2: **TODAY IS A SPECIAL DAY** :star2:\n\nToday is *Easter*\n\nCelebrating the resurrection of Jesus Christ from the dead.")
        elif today == good_friday_date:
            await self.bot.get_channel(CHANNEL_ID).send(":star2: **TODAY IS A SPECIAL DAY** :star2:\n\nToday is *Good Friday*\n\nCommemorating the crucifixion of Jesus Christ and his death at Calvary.")
        elif today == palm_sunday_date:
            await self.bot.get_channel(CHANNEL_ID).send(":star2: **TODAY IS A SPECIAL DAY** :star2:\n\nToday is *Palm Sunday*\n\nCommemorates Jesus's triumphant entry into Jerusalem.")
        elif today == ash_wednesday_date:
            await self.bot.get_channel(CHANNEL_ID).send(":star2: **TODAY IS A SPECIAL DAY** :star2:\n\nToday is *Ash Wednesday*\n\nMarks the start of the Lenten period of fasting and penance.")
        elif today == ascension_date:
            await self.bot.get_channel(CHANNEL_ID).send(":star2: **TODAY IS A SPECIAL DAY** :star2:\n\nToday is *Ascension Day*\n\nCelebrates the Ascension of Jesus Christ into heaven.")
        elif today == pentecost_date:
            await self.bot.get_channel(CHANNEL_ID).send(":star2: **TODAY IS A SPECIAL DAY** :star2:\n\nToday is *Pentecost*\n\nCelebrates the descent of the Holy Spirit upon the Apostles and other followers of Jesus.")
        elif today == corpus_christi_date:
            await self.bot.get_channel(CHANNEL_ID).send(":star2: **TODAY IS A SPECIAL DAY** :star2:\n\nToday is *Corpus Christi*\n\nHonors the Holy Eucharist and the real presence of the body and blood of Jesus Christ.")
        elif (today.month, today.day) in fixed_holidays:
            await self.bot.get_channel(CHANNEL_ID).send(f":star2: **TODAY IS A SPECIAL DAY** :star2:\n\nToday is {fixed_holidays[today.month, today.day]}")
        else:
            print("[DEBUG] Today is not a special day")
