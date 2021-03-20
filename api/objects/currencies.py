from enum import Enum


class Type(Enum):
    CRYPTO = 'crypto'
    FIAT = 'fiat'


class Currency:
    def __init__(self, code: str, precision: int):
        self.code = code.upper()
        self.precision = precision
        self.type = None

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.code == other.code and self.type == other.type
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.code)


class CryptoCurrency(Currency):
    def __init__(self, code, precision):
        super().__init__(code, precision)
        self.type = Type.CRYPTO


class FiatCurrency(Currency):
    def __init__(self, code, precision):
        super().__init__(code, precision)
        self.type = Type.FIAT
