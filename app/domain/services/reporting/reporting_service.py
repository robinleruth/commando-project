import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from math import sqrt
from math import ceil
from dataclasses import dataclass
from dataclasses import field
from matplotlib.figure import Figure

from app.domain.services.reporting.var.var_service import VarService
from app.domain.services.reporting.var.var_service_factory import var_service_factory
from app.domain.services.reporting.var.var_parametrique_service import VarParametriqueService
from app.domain.services.portfolio.portfolio_service import PortfolioService
from app.infrastructure.config import app_config
from app.infrastructure.log import logger


@dataclass
class ReportingService:
    ptf_service: PortfolioService
    var_service: VarService = None
    value_at_risk: float = None
    max_draw_down: float = None
    vol_annu: float = None
    perf_periode: float = None
    perf_annu: float = None
    sharpe_ratio: float = None
    risk_free_rate: float = 0.0
    base_100: pd.DataFrame = None

    def compute_max_draw_down(self) -> float:
        logger.info('ReportingService computing max_drawdown....')
        if self.max_draw_down is None:
            df: pd.DataFrame = self.ptf_service.ptf_to_df()

            roll_max = df[app_config.SPOT].cummax()
            df['roll_max'] = roll_max
            daily_dd = df[app_config.SPOT]/roll_max - 1.0
            df['daily_dd'] = daily_dd
            max_dd = df['daily_dd'].cummin()
            df['max_daily_dd'] = max_dd
            self.max_draw_down =  df['max_daily_dd'].iloc[-1]
        return self.max_draw_down

    def compute_vol(self) -> float:
        if self.vol_annu is None:
            logger.info('ReportingService computing annual volatility....')
            df: pd.DataFrame = self.ptf_service.ptf_to_df()
            df['perf'] = df[app_config.SPOT].pct_change()
            self.vol_annu = df['perf'].std() * sqrt(252)
        return self.vol_annu

    def compute_perf_annu(self) -> float:
        logger.info('ReportingService computing annual return....')
        if self.perf_annu is None:
            df: pd.DataFrame = self.ptf_service.ptf_to_df()
            df = df.fillna(0)
            lst = df[app_config.SPOT].tolist()
            try:
                self.perf_periode = (lst[len(lst) - 1] - lst[0] ) / lst[0]
            except ZeroDivisionError:
                self.perf_periode = 0
            nb_days = len(df[app_config.AS_OF_DATE])
            perf_daily = (1 + self.perf_periode) ** (1 / nb_days) - 1
            self.perf_annu = (1 + perf_daily) ** 365 - 1
        return self.perf_annu

    def compute_sharpe_ratio(self) -> float:
        logger.info('ReportingService computing sharpe ratio....')
        if self.sharpe_ratio is None:
            self.compute_perf_annu()
            self.compute_vol()
            self.sharpe_ratio = (self.perf_annu - self.risk_free_rate) / self.vol_annu
        return self.sharpe_ratio

    def compute_base_100(self) -> pd.DataFrame:
        logger.info('ReportingService computing base 100....')
        if self.base_100 is None:
            df: pd.DataFrame = self.ptf_service.ptf_to_df()
            df['perf'] = df[app_config.SPOT].pct_change()
            df['base_100'] = 100*np.nan_to_num(1 + df['perf'].cumsum(), nan=1)
            self.base_100 = df
        return self.base_100

    def generate_graph(self) -> Figure:
        if self.base_100 is None:
            self.compute_base_100()
        gridsize = (5, 2)
        fig = plt.figure(figsize=(12, 8))
        ax1 = plt.subplot2grid(gridsize, (0,0),
                               colspan=2,
                               rowspan=2)
        ax1.plot(self.base_100[app_config.AS_OF_DATE], self.base_100['base_100'])
        ax1.set_ylabel('Values')
        ax1.set_title('Base 100')
        ax1.set_xlabel('Dates')
        nb_items = ceil(len(self.base_100[app_config.AS_OF_DATE].tolist()) / 6)
        ax1.set_xticks(self.base_100[app_config.AS_OF_DATE].tolist()[::nb_items])

        ax2 = plt.subplot2grid(gridsize, (3,0),
                               colspan=2,
                               rowspan=2)
        ax2.plot(self.base_100[app_config.AS_OF_DATE], self.base_100[app_config.SPOT])
        ax2.set_ylabel('Values')
        ax2.set_title('Not base 100')
        ax2.set_xlabel('Dates')
        nb_items = ceil(len(self.base_100[app_config.AS_OF_DATE].tolist()) / 6)
        ax2.set_xticks(self.base_100[app_config.AS_OF_DATE].tolist()[::nb_items])
        return fig

    def compute_var(self, parametric: bool = True):
        if self.value_at_risk is None:
            if parametric:
                self.var_service = VarParametriqueService(self.compute_vol())
            else:
                self.var_service = None
            self.value_at_risk = self.var_service.get_value_at_risk()
        return self.value_at_risk
