from datetime import datetime, timedelta

from app.database.transactions import *
from app.externals.sumup import *


def update_transactions(conn, per_request_limit: int = 1000):
    latest_transaction = get_latest_transaction(conn)
    if latest_transaction is None:
        latest_date =  datetime.fromisoformat("2020-01-01T00:00:00")
    else:
        latest_date = latest_transaction[-1] + timedelta(milliseconds=1)

    full_api_response = True
    while full_api_response:
        new_transactions = get_transactions(latest_date, per_request_limit)
        add_transactions(new_transactions, conn)
        latest_date = datetime.fromisoformat(max([transaction.transaction_timestamp.strftime(r"%Y-%m-%dT%H:%M:%S.%f") for transaction in new_transactions])) + timedelta(milliseconds=1)
        if len(new_transactions) != per_request_limit:
            full_api_response = False



