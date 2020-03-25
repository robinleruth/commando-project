import unittest

from app.domain.model.portfolio.portfolio_no_short import PortfolioNoShort
from app.domain.model.side import Side


class TestPortfolioNoShortAllowed(unittest.TestCase):
    def setUp(self):
        self.portfolio = PortfolioNoShort(
            money=1000,
            asset_value=105,
            asset_perf=0.05
        )

    def tearDown(self):
        pass

    def test_buy_then_sell(self):
        self.portfolio.make_operation(Side.BUY, 1, transaction_fee=5)
        self.assertEqual(1, len(self.portfolio.positions))
        self.portfolio.make_operation(Side.SELL, 1, transaction_fee=0)
        self.assertEqual(0, len(self.portfolio.positions))
        self.portfolio.compute_liquid_value()
        self.assertEqual(995, self.portfolio.liquidative_value)

    def test_sell_first_error(self):
        exc= None
        try:
            self.portfolio.make_operation(Side.SELL, 1, transaction_fee=0)
        except Exception as e:
            exc = e
        self.assertTrue(exc is not None)


if __name__ == '__main__':
    unittest.main(verbosity=2)
