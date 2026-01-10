import os
import requests
from dotenv import load_dotenv
import json

load_dotenv(".env")



def get_transactions(oldest_date : str = None):

    header = {
        "Authorization" : f"Bearer {os.getenv('SUMUP_API_KEY')}"
    }

    response = requests.get(
        f"https://api.sumup.com/v2.1/merchants/{os.getenv("MERCHANT_CODE")}/transactions/history?limit=10&statuses[]=SUCCESSFUL&statuses[]=REFUNDED&oldest_time={oldest_date}", headers = header)


    if response.status_code != 200:
        raise Exception(f"Error Connecting to API: {response.text}")
    
    required_columns = ["transaction_code", "amount", "status", "payment_type", "entry_mode", "timestamp"]

    transactions_json = response.json()["items"]

    transactions = [{key:value for key, value in transaction.items() if key in required_columns} for transaction in transactions_json]

    return transactions


def get_transaction_products(transaction_codes : list[str]):

    header = {
        "Authorization" : f"Bearer {os.getenv('SUMUP_API_KEY')}"
    }

    transaction_products = []

    for transaction in transaction_codes:
        response = requests.get(f"https://api.sumup.com/v2.1/merchants/{os.getenv("MERCHANT_CODE")}/transactions?transaction_code={transaction}", headers = header)

        if response.status_code != 200:
            raise Exception(f"Error Connecting to API: {response.text}")
        
        print(response.json())

    return 


# Need to look into GoodTill API


transactions = get_transactions("2024-01-01T00:00:00Z")
print(transactions)

codes = []
for transaction in transactions:
    codes.append(transaction["transaction_code"])

print(get_transaction_products(codes))

