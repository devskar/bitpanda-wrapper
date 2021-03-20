from enum import Enum


class Side(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class Order:
    def __init__(self, instrument_code, side: Side, type, amount):
        self.instrument_code = instrument_code
        self.side = side
        self.type = type
        self.amount = amount
