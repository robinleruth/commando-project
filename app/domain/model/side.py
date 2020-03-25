from enum import Enum


class Side(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'
    OTHER = 'OTHER'
