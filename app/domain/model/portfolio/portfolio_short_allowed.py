from app.domain.model.portfolio.portfolio import Portfolio
from app.domain.model.side import Side
from app.domain.model.not_enough_money_exception import NotEnoughMoneyException
from app.domain.model.position import Position


class PortfolioShortAllowed(Portfolio):
    def make_operation(self, side: Side, qty: float, transaction_fee: float,
                       take_profit: float = None, stop_loss: float = None):
        if side is Side.OTHER:
            return
        notional = qty * self.asset_value
        if notional > self.money:
            raise NotEnoughMoneyException(f'Cannot {side} {qty} because {notional} > {self.money}')
        self.money -= notional + transaction_fee
        pos = Position(
            as_of_date=self.as_of_date,
            qty=qty,
            side=side,
                pos_value=notional,
                take_profit=take_profit,
                stop_loss=stop_loss
        )
        self.positions.append(pos)
