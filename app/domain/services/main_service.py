import json
import numpy as np
import pandas as pd

from matplotlib.figure import Figure
from dataclasses import dataclass
from dataclasses import asdict

from app.domain.services.data.data_service import DataService
from app.domain.services.portfolio.portfolio_service import PortfolioService
from app.domain.services.strategy.strategy_service import StrategyService
from app.domain.services.strategy.strategy_service_factory import strategy_service_factory
from app.domain.services.reporting.reporting_service import ReportingService
from app.infrastructure.log import logger


@dataclass
class MainService:
    data_service: DataService
    portfolio_service: PortfolioService
    strategy_service: StrategyService
    reporting_service: ReportingService

    def __init__(self,
                 data_service,
                 portfolio_service,
                 strategy_service):
        logger.info('MainService init ...')
        self.data_service = data_service
        self.strategy_service = strategy_service
        self.portfolio_service = portfolio_service

    def evaluate_all(self):
        self.portfolio_service.evaluate_all()

    def get_reporting(self) -> Figure:
        self.reporting_service = ReportingService(self.portfolio_service)
        self.reporting_service.compute_max_draw_down()
        self.reporting_service.compute_vol()
        self.reporting_service.compute_perf_annu()
        self.reporting_service.compute_sharpe_ratio()
        self.reporting_service.compute_base_100()
        self.reporting_service.compute_var()
        fig = self.reporting_service.generate_graph()
        return fig

    @property
    def serialize(self):
        return {
            'positions': self.portfolio_service.serialize['portfolio'],
            'value_at_risk': self.reporting_service.value_at_risk,
            'max_drawdown': self.reporting_service.max_draw_down,
            'volatility': self.reporting_service.vol_annu,
            'sharpe_ratio': self.reporting_service.sharpe_ratio
        }

    def get_final_portfolio_dataframe(self) -> pd.DataFrame:
        j = self.serialize
        df = pd.DataFrame.from_dict(j['positions'])
        df['level_0'] = [i for i in range(len(df))]
        s = df['positions'].apply(pd.Series).stack().to_frame()
        df_positions = pd.DataFrame(list(s[0]), index=s.index)
        df_positions.rename(columns={'as_of_date': 'as_of_date_init'}, inplace=True)
        df_temp = pd.DataFrame({col: np.repeat(df[col].values, df['positions'].str.len() + 1) for col in df.columns.drop('positions')})
        df_temp['level_1'] = df_temp.groupby('level_0').cumcount()
        df_temp = df_temp.set_index(['level_0', 'level_1'])
        df_positions.index.rename(['level_0', 'level_1'], inplace=True)
        df_final = pd.merge(df_temp, df_positions, how='left', left_index=True, right_index=True)
        df_final = df_final.fillna('')
        return df_final
