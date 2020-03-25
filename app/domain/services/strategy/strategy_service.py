import datetime as dt

from abc import ABCMeta
from abc import abstractmethod

from app.domain.model.side import Side


class StrategyService(metaclass=ABCMeta):
    @abstractmethod
    def evaluate(self, date: dt.datetime) -> Side:
        pass
