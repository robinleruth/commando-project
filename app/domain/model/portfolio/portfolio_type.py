from enum import Enum


class PortfolioType(str, Enum):
    SHORT_ALLOWED = 'SHORT_ALLOWED'
    NO_SHORT_ALLOWED = 'NO_SHORT_ALLOWED'
