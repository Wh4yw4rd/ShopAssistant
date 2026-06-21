from datetime import datetime, timedelta

from database.transactions_db import *
from externals.sumup import *
from models.errors import InvalidDateRange


def update_transactions(conn, per_request_limit: int = 1000):
    num_added = 0
    try:
        latest_transaction = get_latest_transaction(conn)
        latest_id = latest_transaction[0]

    except EmptyTransactionTable:
        first_transaction = get_first_transaction()
        latest_id = first_transaction[0].transaction_id
        add_transactions(first_transaction, conn)
        num_added += 1

    next = None

    full_api_response = True
    while full_api_response:
        if next == None:
            new_transactions, next = get_transactions(latest_id, per_request_limit)
        else:
            new_transactions, next = get_transactions(latest_id, per_request_limit, use_href = True, href = next)
        add_transactions(new_transactions, conn)
        num_added += len(new_transactions)
        if len(new_transactions) != per_request_limit:
            full_api_response = False
    
    return num_added


def transaction_range(start: datetime, end: datetime, conn):
    if start >= end:
        raise InvalidDateRange()
    
    data = transaction_date_range(start, end, conn)
    return data


