import datetime as dt

from dataclasses import dataclass
from dataclasses import field

from app.domain.model.side import Side


@dataclass
class Position:
    as_of_date: dt.datetime = dt.datetime.now()
    side: Side = Side.OTHER
    qty: int = 0
    pos_value: float = 0.0
    take_profit: float = None
    stop_loss: float = None
    initial_pos_value: float = 0.0

    def __post_init__(self):
        self.initial_pos_value = self.pos_value

    def compute_pos_value(self, perf):
        if self.side is Side.BUY:
            self.pos_value *= 1 + perf
        elif self.side is Side.SELL:
            self.pos_value *= 1 - perf
        else:
            raise Exception('Side is neither BUY or SELL')

    @property
    def close_position(self) -> bool:
        if self._evalute_take_profit() or self._evalute_stop_loss():
            return True
        else:
            return False

    def _evalute_take_profit(self) -> bool:
        if self.take_profit is None:
            return False
        perf = self._evaluate_perf()
        if perf > self.take_profit:
            return True
        else:
            return False

    def _evalute_stop_loss(self) -> bool:
        if self.stop_loss is None:
            return False
        perf = self._evaluate_perf()
        if perf < self.stop_loss:
            return True
        else:
            return False

    def _evaluate_perf(self) -> float:
        perf = (self.pos_value - self.initial_pos_value) / self.initial_pos_value
        if self.side is Side.SELL:
            perf *= -1
        return perf

    @property
    def serialize(self):
        return {
            'as_of_date': self.as_of_date.strftime('%Y-%m-%d'),
            'side': str(self.side),
            'qty': float(self.qty),
            'pos_value': float(self.pos_value),
            'take_profit': float(self.take_profit or 0),
            'stop_loss': float(self.stop_loss or 0),
            'initial_pos_value': float(self.initial_pos_value)
        }
