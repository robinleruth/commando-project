from pydantic import BaseModel
from datetime import date
from typing import List

from app.interface.api.schemas.position_schema import PositionSchema


class PortfolioSchema(BaseModel):
    as_of_date: date
    money: float
    asset_value: float
    positions: List[PositionSchema]
    liquidative_value: float
    asset_perf: float
    open: float
    high: float
    low: float
    close: float
    turnover: float
    volatility: float
