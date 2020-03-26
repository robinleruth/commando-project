from enum import Enum


class AvailableStocks(str, Enum):
    MOCK = 'MOCK'
    SP500 = 'SP500'
