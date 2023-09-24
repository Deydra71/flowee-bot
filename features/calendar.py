from discord.ext import commands
from datetime import datetime, timedelta, date
from dateutil.easter import easter
import asyncio

CHANNEL_ID = 1117869477669916803

class ChristianCalendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("[DEBUG] Initializing ChristianCalendar")  # Debug print
        self.task = self.bot.loop.create_task(self.check_date())

    def cog_unload(self):
        self.task.cancel()

    async def check_date(self):
        print("[DEBUG] Inside check_date method")  # Debug print

        # Immediately announce all defined dates after bot starts for testing
        current_year = datetime.now().year

        # Movable feast dates
        await self.announce_date(current_year, easter(current_year).month, easter(current_year).day)
        await self.announce_date(current_year, (easter(current_year) - timedelta(days=46)).month, (easter(current_year) - timedelta(days=46)).day)
        await self.announce_date(current_year, (easter(current_year) - timedelta(days=7)).month, (easter(current_year) - timedelta(days=7)).day)
        await self.announce_date(current_year, (easter(current_year) - timedelta(days=2)).month, (easter(current_year) - timedelta(days=2)).day)
        await self.announce_date(current_year, (easter(current_year) + timedelta(days=39)).month, (easter(current_year) + timedelta(days=39)).day)
        await self.announce_date(current_year, (easter(current_year) + timedelta(days=49)).month, (easter(current_year) + timedelta(days=49)).day)
        await self.announce_date(current_year, (easter(current_year) + timedelta(days=60)).month, (easter(current_year) + timedelta(days=60)).day)

        # Fixed holidays
        fixed_holidays_dates = [
            (1, 6),
            (2, 2),
            (2, 14),
            (3, 25),
            (6, 26),
            (10, 4),
            (10, 31),
            (11, 1),
            (11, 2),
            (12, 25),
            (12, 26)
        ]
        for date in fixed_holidays_dates:
            await self.announce_date(current_year, date[0], date[1])

        # Now let the bot proceed to its usual behavior of checking dates daily
        while True:
            now = datetime.now()
            next_time = now.replace(hour=8, minute=0, second=0)
            if now.hour >= 8:
                next_time += timedelta(days=1)
            to_wait = (next_time - now).seconds
            print(f"[DEBUG] Sleeping for {to_wait} seconds")  # Debug print
            await asyncio.sleep(to_wait)
            await self.announce_date()

    async def announce_date(self, year=None, month=None, day=None): 
        print("[DEBUG] Inside announce_date method")  # Debug print

        if year and month and day:
            today = date(year, month, day)
        else:
            today = datetime.now().date()
        
        print(f"[DEBUG] Today's date is: {today}")  # Debug print

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
            await self.bot.get_channel(CHANNEL_ID).send(":star2: **TODAY IS A SPECIAL DAY** :star2:\nToday is Corpus Christi - Honors the Holy Eucharist and the real presence of the body and blood of Jesus Christ.")
        elif today in fixed_holidays:
            await self.bot.get_channel(CHANNEL_ID).send(f":star2: **TODAY IS A SPECIAL DAY** :star2:\nToday is {fixed_holidays[today]}")
        else:
            print("[DEBUG] Today is not a special day")  # Debug print
