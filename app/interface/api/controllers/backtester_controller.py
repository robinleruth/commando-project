import os
import uuid

from fastapi import APIRouter
from fastapi import HTTPException

from app.interface.api.schemas.strategy_schema import StrategySchemaOut
from app.interface.api.schemas.strategy_schema import StrategySchemaIn
from app.domain.model.portfolio.portfolio_type import PortfolioType
from app.domain.services.portfolio.portfolio_service import PortfolioService
from app.domain.services.strategy.random_strategy import RandomStrategy
from app.domain.services.strategy.strategy_service_factory import strategy_service_factory
from app.domain.services.data.data_service import DataService
from app.domain.services.main_service import MainService
from app.infrastructure.config import app_config


router = APIRouter()


@router.post('/', response_model=StrategySchemaOut)
async def backtest_strategy(params: StrategySchemaIn):
    transaction_fee = params.transaction_fee
    initial_capital = params.initial_capital
    take_profit = params.take_profit if params.take_profit != 0 else None
    stop_loss = params.stop_loss if params.stop_loss != 0 else None
    strategy = params.strategy
    ptf_type = params.ptf_type
    data_service = DataService()
    strategy_service = strategy_service_factory(strategy)
    portfolio_service = PortfolioService(transaction_fee,
                                         strategy_service,
                                         asset_values=data_service.df,
                                         initial_capital=initial_capital,
                                         ptf_type=ptf_type,
                                         take_profit=take_profit,
                                         stop_loss=stop_loss)
    service = MainService(data_service, portfolio_service, strategy_service)
    service.evaluate_all()
    fig = service.get_reporting()
    file_name = uuid.uuid4().hex + '.png'
    file_path = os.path.join(app_config.GRAPH_FOLDER, file_name)
    fig.savefig(file_path)
    ret = service.serialize
    ret['base_100_file_name'] = file_name
    return ret
