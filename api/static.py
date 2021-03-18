from enum import Enum


class Scope(Enum):
    READ = 'Read'
    TRADE = 'Trade'
    WITHDRAW = 'Withdraw'


class Fiat(Enum):
    EURO = 'EUR'
    FRANC = 'CHF'
    POUND = 'GBP'
