from pydantic import BaseModel
from datetime import datetime


class TransactionsDB(BaseModel):
    id: str | None = None
    transaction_id: str
    transaction_code: str
    transaction_timestamp: datetime
    entry_mode: str
    card_type: str | None = None
    amount: float | None = None
    refunded_amount: float | None = None
    payment_type: str
    status: str