import numpy as np
import pandas as pd
import datetime as dt

from dataclasses import dataclass

from app.domain.services.strategy.strategy_service import StrategyService
from app.domain.services.data.data_service import DataService
from app.domain.model.side import Side
from app.infrastructure.config import app_config
from app.infrastructure.log import logger


@dataclass
class MovingAverageStrategyService(StrategyService):
    data_service: DataService
    short_term_trend: int
    long_term_trend: int
    signal_threshold: float = 50
    df: pd.DataFrame = None

    def __post_init__(self):
        self.compute()

    def compute(self):
        logger.info('MovingAverageStrategyService computing signals...')
        self.df = self.data_service.df
        self.df = self.df.set_index(app_config.AS_OF_DATE)
        # Moving averages short_term_trend days and long_term_trend days
        self.df['short_term_trend'] = np.round(self.df[app_config.CLOSE].rolling(f'{self.short_term_trend}D').mean())
        self.df['long_term_trend'] = np.round(self.df[app_config.CLOSE].rolling(f'{self.long_term_trend}D').mean())

        self.df['short_term_trend - long_term_trend'] = self.df['short_term_trend'] - self.df['long_term_trend']

        self.df['Regime'] = np.where(self.df['short_term_trend - long_term_trend'] > self.signal_threshold, 1, 0)
        self.df['Regime'] = np.where(self.df['short_term_trend - long_term_trend'] < -self.signal_threshold, -1, self.df['Regime'])
        logger.info('MovingAverageStrategyService computation done...')

    def evaluate(self, date: dt.datetime) -> Side:
        if self.df.loc[date]['Regime'] == 1:
            return Side.BUY
        elif self.df.loc[date]['Regime'] == -1:
            return Side.SELL
        else:
            return Side.OTHER
