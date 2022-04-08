class TransactionMessage:
    def __init__(self, msg_type: str, from_address: str, to_address: str, amount: float, currency: str):
        self.msg_type = msg_type
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.currency = currency