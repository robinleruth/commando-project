import pandas as pd

from copy import deepcopy
from typing import List
from dataclasses import dataclass
from dataclasses import field
from dataclasses import InitVar
from dataclasses import asdict

from app.domain.model.portfolio.portfolio import Portfolio
from app.domain.model.portfolio.portfolio_factory import portfolio_factory
from app.domain.model.portfolio.portfolio_exception import PortfolioException
from app.domain.model.side import Side
from app.domain.model.position import Position
from app.domain.model.portfolio.portfolio_short_allowed import PortfolioShortAllowed
from app.domain.model.portfolio.portfolio_type import PortfolioType
from app.domain.model.not_enough_money_exception import NotEnoughMoneyException
from app.domain.services.strategy.strategy_service import StrategyService
from app.domain.services.strategy.strategy_service_factory import strategy_service_factory
from app.infrastructure.config import app_config
from app.infrastructure.log import logger


@dataclass
class PortfolioService:
    transaction_fee: float = 0
    strategy_service: StrategyService = field(default_factory=strategy_service_factory)
    portfolio: List[Portfolio] = field(default_factory=list)
    asset_values: InitVar[pd.DataFrame] = None
    initial_capital: InitVar[float] = 0
    df: pd.DataFrame = None
    ptf_type: InitVar[PortfolioType] = None
    take_profit: float = None
    stop_loss: float = None

    def __post_init__(self, asset_values: pd.DataFrame, initial_capital: float, ptf_type: PortfolioType):
        logger.info('Portfolio service init...')
        if ptf_type is None:
            raise Exception('ptf_type cannot be None')
        if asset_values is not None:
            for i in asset_values.index:
                if i == 0:
                    ptf = PortfolioShortAllowed(
                        as_of_date=asset_values.at[i, app_config.AS_OF_DATE],
                        money=initial_capital,
                        asset_value=asset_values.at[i, app_config.SPOT],
                        open_value=asset_values.at[i, app_config.OPEN],
                        high_value=asset_values.at[i, app_config.HIGH],
                        low_value=asset_values.at[i, app_config.LOW],
                        close_value=asset_values.at[i, app_config.CLOSE],
                        turnover=asset_values.at[i, app_config.TURNOVER],
                        volatility=asset_values.at[i, app_config.VOLATILITY]
                    )
                else:
                    ptf = portfolio_factory(self.portfolio[-1],
                                            asset_values.at[i, app_config.SPOT],
                                            asset_values.at[i, app_config.AS_OF_DATE],
                                            ptf_type,
                                            open_value=asset_values.at[i, app_config.OPEN],
                                            high_value=asset_values.at[i, app_config.HIGH],
                                            low_value=asset_values.at[i, app_config.LOW],
                                            close_value=asset_values.at[i, app_config.CLOSE],
                                            turnover=asset_values.at[i, app_config.TURNOVER],
                                            volatility=asset_values.at[i, app_config.VOLATILITY]
                                            )
                self.portfolio.append(ptf)

    def evaluate(self, ptf: Portfolio,
                 previous_positions: List[Position],
                 previous_money: float=None):
        if previous_money:
            ptf.money = previous_money
        ptf.positions = deepcopy(previous_positions)
        ptf.compute_liquid_value()
        ptf.close_position()
        side: Side = self.strategy_service.evaluate(ptf.as_of_date)
        try:
            ptf.make_operation(side, 1,
                               self.transaction_fee,
                               self.take_profit,
                               self.stop_loss)
        except (PortfolioException, NotEnoughMoneyException) as e:
            logger.error(e)

    def evaluate_all(self):
        logger.info('Portfolio service evaluate_all...')
        previous_positions: List[Position] = []
        previous_money = None
        for ptf in self.portfolio:
            self.evaluate(ptf, previous_positions, previous_money)
            previous_positions = ptf.positions
            previous_money = ptf.money

    def ptf_to_df(self):
        ''' TODO: If data more than daily, take only the close or return all info (OPEN/ CLOSE/ ETC) '''
        if self.df is None:
            self.df = pd.DataFrame(list(zip([i.as_of_date for i in self.portfolio],
                                            [i.liquidative_value for i in self.portfolio],
                                            [i.asset_value for i in self.portfolio])),
                                   columns=[app_config.AS_OF_DATE, app_config.SPOT, 'asset_value'])
        return self.df

    @property
    def serialize(self):
        return {
            'portfolio': [i.serialize for i in self.portfolio]
        }
