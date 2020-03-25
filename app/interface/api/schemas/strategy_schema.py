from pydantic import BaseModel
from typing import List
from typing import Union

from app.interface.api.schemas.position_schema import PositionSchema
from app.interface.api.schemas.portfolio_schema import PortfolioSchema
from app.domain.model.available_strategy import AvailableStrategy
from app.domain.model.portfolio.portfolio_type import PortfolioType


class StrategySchema(BaseModel):
    pass


class StrategySchemaIn(StrategySchema):
    stock: str
    strategy: AvailableStrategy
    ptf_type: PortfolioType
    params: List[Union[str, float]]
    transaction_fee: float
    # function_to_optimize: str
    # optim_algorithm: str
    initial_capital: float
    take_profit: float
    stop_loss: float


class StrategySchemaOut(StrategySchema):
    base_100_file_name: str
    value_at_risk: float
    max_drawdown: float
    volatility: float
    sharpe_ratio: float
    positions: List[PortfolioSchema]
