import unittest
import pandas as pd
import datetime as dt

from app.domain.services.portfolio.portfolio_service import PortfolioService
from app.domain.services.strategy.mock_strategy_service import MockStrategyService
from app.domain.model.portfolio.portfolio_type import PortfolioType
from app.infrastructure.config import app_config


class TestPortfolioService(unittest.TestCase):
    def setUp(self):
        dates = ['2020-03-01', '2020-03-02', '2020-03-03']
        dates = list(map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d"), dates))
        spot = [100, 105, 90]
        df = pd.DataFrame(list(zip(dates, spot)), columns=[app_config.AS_OF_DATE, app_config.SPOT])
        strat_service = MockStrategyService()
        self.ptf_service = PortfolioService(asset_values=df,
                                            initial_capital=1000,
                                            ptf_type=PortfolioType.SHORT_ALLOWED,
                                            strategy_service=strat_service)
        print()

    def tearDown(self):
        pass

    def test_evaluate_all(self):
        self.ptf_service.evaluate_all()
        ptf = self.ptf_service.portfolio[0]
        self.assertEqual(1000, ptf.liquidative_value)
        ptf = self.ptf_service.portfolio[1]
        self.assertEqual(1005, ptf.liquidative_value)
        ptf = self.ptf_service.portfolio[2]
        self.assertEqual(975, ptf.liquidative_value)

    def test_to_df(self):
        df = self.ptf_service.ptf_to_df()


if __name__ == '__main__':
    unittest.main(verbosity=2)
