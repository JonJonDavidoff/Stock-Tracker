import datetime
import pytz
import holidays

tz = pytz.timezone('US/Eastern')
us_holidays = holidays.US()


class Market:
    def __init__(self):
        pass

    def is_open(self, now=None):
        if not now:
            now = datetime.datetime.now(tz)
        openTime = datetime.time(hour=9, minute=30, second=0)
        closeTime = datetime.time(hour=16, minute=0, second=0)
        # If a holiday
        if now.strftime('%Y-%m-%d') in us_holidays:
            return False
        # If before 0930 or after 1600
        if (now.time() < openTime) or (now.time() > closeTime):
            return False
        # If it's a weekend
        if now.date().weekday() > 4:
            return False

        return True
