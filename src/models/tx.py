from datetime import datetime
from typing import List


class Transaction:
    def __init__(self, tx_hash: str, time: datetime, fee: float, fee_currency: str):
        self.tx_hash = tx_hash
        self.time = time
        self.fee = fee
        self.fee_currency = fee_currency
        self.messages: List[TransactionMessage] = []


class TransactionMessage:
    def __init__(self, msg_type: str, from_address: str, to_address: str, amount: float, currency: str):
        self.msg_type = msg_type
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.currency = currency
