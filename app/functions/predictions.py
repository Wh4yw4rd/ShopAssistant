from datetime import datetime, timedelta

from app.database.transactions import *


def moving_7_day_average(day: datetime, conn):
    data = transaction_date_range(day - timedelta(days=8), day, conn)
    average = sum([transaction[6] for transaction in data]) / 7
    return average