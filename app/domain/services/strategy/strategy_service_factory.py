from app.domain.services.strategy.strategy_service import StrategyService
from app.domain.services.strategy.mock_strategy_service import MockStrategyService
from app.domain.services.strategy.random_strategy import RandomStrategy
from app.domain.services.strategy.moving_average_strategy_service import MovingAverageStrategyService
from app.domain.services.data.data_service import DataService
from app.domain.model.available_strategy import AvailableStrategy


def strategy_service_factory(strat: AvailableStrategy, data_service: DataService, *args) -> StrategyService:
    if strat is AvailableStrategy.RANDOM_SIGNAL:
        return RandomStrategy()
    elif strat is AvailableStrategy.MOVING_AVERAGE:
        return MovingAverageStrategyService(data_service, *args)
    return None
