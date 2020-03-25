import datetime as dt

from app.domain.model.side import Side
from app.domain.services.strategy.strategy_service import StrategyService


class MockStrategyService(StrategyService):
    def evaluate(self, date: dt.datetime) -> Side:
        return Side.BUY
