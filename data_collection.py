import requests
import json

from config import sumup_api
from models import Transaction


def get_transactions(oldest_date : str = None):

    header = {
        "Authorization" : f"Bearer {sumup_api["key"]}"
    }

    response = requests.get(
        f"https://api.sumup.com/v2.1/merchants/{sumup_api["merchant_code"]}/transactions/history?limit=10&statuses[]=SUCCESSFUL&statuses[]=REFUNDED&oldest_time={oldest_date}", headers = header)


    if response.status_code != 200:
        raise Exception(f"Error Connecting to API: {response.text}")
    
    required_columns = ["transaction_code", "amount", "status", "payment_type", "entry_mode", "timestamp"]

    transactions_json = response.json()["items"]

    transactions = [Transaction(**{key:value for key, value in transaction.items() if key in required_columns}) for transaction in transactions_json]

    return transactions


# TODO:
# Need to look into GoodTill API

def get_transaction_products(transaction_codes : list[str]):

    header = {
        "Authorization" : f"Bearer {sumup_api["key"]}"
    }

    transaction_products = []

    for transaction in transaction_codes:
        response = requests.get(f"https://api.sumup.com/v2.1/merchants/{sumup_api["merchant_code"]}/transactions?transaction_code={transaction}", headers = header)

        if response.status_code != 200:
            raise Exception(f"Error Connecting to API: {response.text}")
        
        print(response.json())

    return 

