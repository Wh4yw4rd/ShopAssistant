import requests
from datetime import datetime, timedelta

from app.core.config import sumup_api
from app.schemas.data_schemas import TransactionsDB


def get_transactions(oldest_date: datetime = datetime.now() - timedelta(days=7), limit: int = 1000):
    header = {
        "Authorization": f"Bearer {sumup_api["key"]}"
    }

    url = f"https://api.sumup.com/v2.1/merchants/{sumup_api["merchant_code"]}/transactions/history?limit={limit}&statuses[]=SUCCESSFUL&statuses[]=REFUNDED&oldest_time={oldest_date.isoformat()}"

    response = requests.get(url, headers=header)

    if response.status_code != 200:
        raise Exception("Error Connecting to SumUp API", response.json())
    
    transactions = response.json()["items"]
    transactions = [TransactionsDB(transaction_id = transaction["id"], 
                                   transaction_code = transaction["transaction_code"],
                                   transaction_timestamp = transaction["timestamp"],
                                   entry_mode = transaction["entry_mode"],
                                   card_type = transaction.get("card_type"),
                                   amount = transaction.get("amount"),
                                   refunded_amount = transaction.get("refunded_amount"),
                                   payment_type = transaction["payment_type"],
                                   status = transaction["status"]) for transaction in transactions]
    
    return transactions

    
    
