import random
import datetime as dt

from dataclasses import dataclass
from dataclasses import field
from dataclasses import asdict
from typing import List
from abc import ABCMeta
from abc import abstractmethod

from app.domain.model.position import Position
from app.domain.model.not_enough_money_exception import NotEnoughMoneyException
from app.domain.model.side import Side


@dataclass
class Portfolio(metaclass=ABCMeta):
    as_of_date: dt.datetime = dt.datetime.now()
    money: float = 0
    asset_value: float = 0
    positions: List[Position] = field(default_factory=list)
    liquidative_value: float = 0
    asset_perf: float = 0
    open_value: float = 0
    high_value: float = 0
    low_value: float = 0
    close_value: float = 0
    turnover: float = 0
    volatility: float = 0

    def compute_liquid_value(self):
        self.liquidative_value = self.money
        for position in self.positions:
            position.compute_pos_value(self.asset_perf)
            self.liquidative_value += position.pos_value

    def close_position(self, force=False):
        mask = []
        for position in self.positions:
            if position.close_position or force:
                self.money += position.pos_value
                mask.append(False)
            else:
                mask.append(True)
        self.positions = [d for d, s in zip(self.positions, mask) if s]

    @abstractmethod
    def make_operation(self, side: Side, qty: float, transaction_fee: float,
                       take_profit: float = None, stop_loss: float = None):
        pass

    @property
    def serialize(self):
        return {
            'as_of_date': self.as_of_date.strftime('%Y-%m-%d'),
            'money': float(self.money),
            'asset_value': float(self.asset_value),
            'positions': [i.serialize for i in self.positions],
            'liquidative_value': float(self.liquidative_value),
            'asset_perf': float(self.asset_perf),
            'open': round(float(self.open_value), 2),
            'high': round(float(self.high_value), 2),
            'low': round(float(self.low_value), 2),
            'close': round(float(self.close_value), 2),
            'turnover': round(float(self.turnover), 2),
            'volatility': round(float(self.volatility), 2)
        }
