from enum import Enum


class AvailableStrategy(str, Enum):
    RANDOM_SIGNAL = 'RANDOM_SIGNAL'
    MOVING_AVERAGE = 'MOVING_AVERAGE'
