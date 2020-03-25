import datetime as dt

from copy import deepcopy

from app.domain.model.portfolio.portfolio import Portfolio
from app.domain.model.portfolio.portfolio_short_allowed import PortfolioShortAllowed
from app.domain.model.portfolio.portfolio_type import PortfolioType
from app.domain.model.portfolio.portfolio_no_short import PortfolioNoShort


def portfolio_factory(ptf: Portfolio, asset_value: float, as_of_date: dt.datetime, ptf_type: PortfolioType) -> Portfolio:
    perf = (asset_value - ptf.asset_value) / ptf.asset_value
    if ptf_type is PortfolioType.SHORT_ALLOWED:
        return PortfolioShortAllowed(
            as_of_date=as_of_date,
            money=ptf.money,
            asset_value=asset_value,
            positions=deepcopy(ptf.positions),
            asset_perf=perf
        )
    else:
        return PortfolioNoShort(
            as_of_date=as_of_date,
            money=ptf.money,
            asset_value=asset_value,
            positions=deepcopy(ptf.positions),
            asset_perf=perf
        )
