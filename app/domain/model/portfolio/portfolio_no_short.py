from dataclasses import dataclass

from app.domain.model.portfolio.portfolio import Portfolio
from app.domain.model.portfolio.portfolio_exception import PortfolioException
from app.domain.model.side import Side
from app.domain.model.position import Position
from app.domain.model.not_enough_money_exception import NotEnoughMoneyException
from app.infrastructure.log import logger


@dataclass
class PortfolioNoShort(Portfolio):
    in_buy_position: bool = False

    def make_operation(self, side: Side, qty: float, transaction_fee: float,
                       take_profit: float = None, stop_loss: float = None):
        if side is Side.OTHER:
            return
        if len(self.positions) > 0:
            self.in_buy_position = True
        if side is Side.SELL and not self.in_buy_position:
            raise PortfolioException('Cannot Sell something not in the portfolio')
        elif side is Side.SELL and self.in_buy_position:
            logger.info('Closing all buy positions because of selling signal')
            self.close_position(force=True)
        else:
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
