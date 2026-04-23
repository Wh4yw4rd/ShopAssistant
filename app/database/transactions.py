from app.schemas.data_schemas import TransactionsDB
from datetime import datetime, timedelta

def get_latest_transaction(conn):
    latest_transaction = """
                        SELECT 
                        transaction_id,
                        transaction_code,
                        transaction_timestamp
                        FROM transactions
                        ORDER BY transaction_timestamp DESC
                        LIMIT 1"""
    
    try:
        with conn.cursor() as cur:
            cur.execute(latest_transaction)
            latest = cur.fetchone()
        
        return latest
    
    except Exception as e:
        raise RuntimeError("Database Error")
    

def add_transactions(transactions: list[TransactionsDB], conn):
    if len(transactions) == 0:
        raise ValueError("No transactions to update.")
    
    add_transactions = """
                    INSERT INTO transactions 
                        (transaction_id, transaction_code, transaction_timestamp, entry_mode, card_type, amount, refunded_amount, payment_type, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    columns = ["transaction_id", "transaction_code", "transaction_timestamp", "entry_mode", "card_type", "amount", "refunded_amount", "payment_type", "status"]

    transactions_to_add = [[getattr(transactions[0], column) for column in columns]]

    for i in range(1, len(transactions)):
        add_transactions += ", (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        transactions_to_add.append([getattr(transactions[i], column) for column in columns])
    
    add_transactions += ";"
    transactions_to_add = tuple([value for transaction in transactions_to_add for value in transaction])

    try:
        with conn.cursor() as cur:
            cur.execute(add_transactions, transactions_to_add)
        
        conn.commit()
    
    except Exception as e:
        conn.rollback()
        raise RuntimeError("Database Error", e)
    
         
def transaction_date_range(start: datetime, end: datetime, conn):
    date_range_filter = """
                        SELECT *
                        FROM transactions
                        WHERE transaction_timestamp >= %s
                        AND transaction_timestamp < %s
                        ORDER BY transaction_timestamp ASC;
                        """
    
    with conn.cursor() as cur:
        cur.execute(date_range_filter, (start, end,))
        transactions = cur.fetchall()
    
    return transactions
    