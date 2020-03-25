from app.domain.services.strategy.strategy_service import StrategyService
from app.domain.services.strategy.mock_strategy_service import MockStrategyService
from app.domain.services.strategy.random_strategy import RandomStrategy
from app.domain.model.available_strategy import AvailableStrategy


def strategy_service_factory(strat: AvailableStrategy) -> StrategyService:
    if strat is AvailableStrategy.RANDOM_SIGNAL:
        return RandomStrategy()
    return None
