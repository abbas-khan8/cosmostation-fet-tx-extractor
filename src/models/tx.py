from datetime import datetime
from typing import List

from src.models.tx_message import TransactionMessage


class Transaction:
    def __init__(
            self,
            tx_hash: str = "undefined",
            valid: bool = False,
            time: datetime = datetime.now(),
            fee: float = -1,
            fee_currency: str = "undefined"
    ):
        self.tx_hash = tx_hash
        self.valid = valid
        self.time = time
        self.fee = fee
        self.fee_currency = fee_currency
        self.messages: List[TransactionMessage] = []


