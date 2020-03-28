import json
import unittest

from app.domain.services.main_service import MainService
from app.domain.services.reporting.var.var_service_factory import var_service_factory
from app.domain.services.data.data_service import DataService
from app.domain.services.data.available_stocks import AvailableStocks
from app.domain.services.portfolio.portfolio_service import PortfolioService
from app.domain.services.strategy.strategy_service_factory import strategy_service_factory
from app.domain.services.strategy.random_strategy import RandomStrategy
from app.domain.model.portfolio.portfolio_type import PortfolioType
from app.infrastructure.data.data_connector_factory import data_connector_factory


class TestMainService(unittest.TestCase):
    def setUp(self):
        transaction_fee = 5
        initial_capital = 10000
        data_connector = data_connector_factory(AvailableStocks.MOCK)
        data_service = DataService(data_connector)
        strategy_service = RandomStrategy()
        portfolio_service = PortfolioService(transaction_fee, strategy_service,
                                             asset_values=data_service.df,
                                             initial_capital=initial_capital,
                                             ptf_type=PortfolioType.SHORT_ALLOWED)
        var_service = var_service_factory()
        self.service = MainService(data_service,
                                   portfolio_service,
                                   strategy_service)

    def tearDown(self):
        pass

    def test_service(self):
        self.service.evaluate_all()
        fig = self.service.get_reporting()
        fig.savefig('test2.png')
        a = self.service.serialize
        with open('test.json', 'w') as f:
            f.write(json.dumps(a))
        df = self.service.get_final_portfolio_dataframe()
        df.to_html('table.html')


if __name__ == '__main__':
    unittest.main(verbosity=2)
