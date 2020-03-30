import datetime as dt

from copy import deepcopy

from app.domain.model.portfolio.portfolio import Portfolio
from app.domain.model.portfolio.portfolio_short_allowed import PortfolioShortAllowed
from app.domain.model.portfolio.portfolio_type import PortfolioType
from app.domain.model.portfolio.portfolio_no_short import PortfolioNoShort


def portfolio_factory(ptf: Portfolio, asset_value: float,
                      as_of_date: dt.datetime,
                      ptf_type: PortfolioType,
                      open_value: float, high_value: float,
                      low_value: float, close_value: float,
                      turnover: float=None, volatility: float=None) -> Portfolio:
    perf = (asset_value - ptf.asset_value) / ptf.asset_value
    if ptf_type is PortfolioType.SHORT_ALLOWED:
        return PortfolioShortAllowed(
            as_of_date=as_of_date,
            money=ptf.money,
            asset_value=asset_value,
            positions=deepcopy(ptf.positions),
            asset_perf=perf,
            open_value=open_value,
            high_value=high_value,
            low_value=low_value,
            close_value=close_value,
            turnover=turnover,
            volatility=volatility
        )
    else:
        return PortfolioNoShort(
            as_of_date=as_of_date,
            money=ptf.money,
            asset_value=asset_value,
            positions=deepcopy(ptf.positions),
            asset_perf=perf,
            open_value=open_value,
            high_value=high_value,
            low_value=low_value,
            close_value=close_value,
            turnover=turnover,
            volatility=volatility
        )
