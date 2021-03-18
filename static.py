from enum import Enum


class Scope(Enum):
    READ = 'Read'
    TRADE = 'Trade'
    WITHDRAW = 'Withdraw'