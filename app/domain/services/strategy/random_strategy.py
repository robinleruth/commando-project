import random
import datetime as dt

from app.domain.services.strategy.strategy_service import StrategyService
from app.domain.model.side import Side


class RandomStrategy(StrategyService):
    def evaluate(self, date: dt.datetime) -> Side:
        r = random.randint(0, 5)
        if r == 0:
            return Side.BUY
        elif r == 1:
            return Side.SELL
        else:
            return Side.OTHER
