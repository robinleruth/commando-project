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
    open_value: float
    high_value: float
    low_value: float
    close_value: float
    turnover: float
    volatility: float
