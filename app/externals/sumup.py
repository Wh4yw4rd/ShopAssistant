import requests
from datetime import datetime, timedelta

from app.core.config import sumup_api


def get_transactions(oldest_date: datetime = datetime.now() - timedelta(days=7)):
    header = {
        "Authorization": f"Bearer {sumup_api["key"]}"
    }

    url = f"https://api.sumup.com/v2.1/merchants/{sumup_api["merchant_code"]}/transactions/history?limit=10&statuses[]=SUCCESSFUL&statuses[]=REFUNDED&oldest_time={oldest_date.isoformat()}"

    response = requests.get(url, headers=header)

    if response.status_code != 200:
        raise Exception("Error Connecting to SumUp API", response.status_code)
    
    transactions = response.json()["items"]
    
    return transactions

    
    
