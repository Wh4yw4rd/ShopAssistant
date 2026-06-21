import requests
from datetime import datetime, timedelta

from core.config import sumup_api
from schemas.data_schemas import TransactionsDB
from models.errors import APIConnectionError


def get_transactions(oldest_ref: str, limit: int = 1000, use_href: bool = False, href: str | None = None):
    header = {
        "Authorization": f"Bearer {sumup_api["key"]}"
    }

    if use_href:
        url = f"https://api.sumup.com/v2.1/merchants/{sumup_api["merchant_code"]}/transactions/history?" + href
    
    else:
        url = f"https://api.sumup.com/v2.1/merchants/{sumup_api["merchant_code"]}/transactions/history?limit={limit}&statuses[]=SUCCESSFUL&statuses[]=REFUNDED&oldest_ref={oldest_ref}&order=ascending"

    response = requests.get(url, headers=header)

    if response.status_code != 200:
        raise APIConnectionError("Unable to connect to external transaction API.")
    

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
    
    if "links" in response.json():
        next = response.json()["links"][0]["href"]
    
    else:
        next = "Done"
    
    return transactions, next


def get_first_transaction():
    header = {
        "Authorization": f"Bearer {sumup_api["key"]}"
    }

    url = f"https://api.sumup.com/v2.1/merchants/{sumup_api["merchant_code"]}/transactions/history?order=ascending&limit=1"

    response = requests.get(url, headers=header)

    if response.status_code != 200:
        raise APIConnectionError("Unable to connect to external transaction API.")
    
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
    
    
