import unittest

from app.domain.model.position import Position
from app.domain.model.side import Side
from app.domain.model.portfolio.portfolio_short_allowed import PortfolioShortAllowed


class TestPortfolioShortAllowed(unittest.TestCase):
    def setUp(self):
        self.portfolio = PortfolioShortAllowed(
            money=1000,
            asset_value=105,
            asset_perf=0.05
        )
        self.transaction_fee = 5
        print()

    def tearDown(self):
        pass

    def test_buy(self):
        self.portfolio.make_operation(Side.BUY, 1, self.transaction_fee)
        self.assertEqual(1, len(self.portfolio.positions))
        self.assertEqual(890, self.portfolio.money)
        pos = self.portfolio.positions[0]
        self.assertEqual(105, pos.pos_value)
        self.portfolio.compute_liquid_value()
        self.assertEqual(1000.25, self.portfolio.liquidative_value)

    def test_buy_two(self):
        self.portfolio.make_operation(Side.BUY, 2, self.transaction_fee)
        self.assertEqual(1, len(self.portfolio.positions))
        self.assertEqual(785, self.portfolio.money)
        pos = self.portfolio.positions[0]
        self.assertEqual(210, pos.pos_value)
        self.portfolio.compute_liquid_value()
        self.assertEqual(1005.5, self.portfolio.liquidative_value)

    def test_sell(self):
        self.portfolio.make_operation(Side.SELL, 1, self.transaction_fee)
        self.assertEqual(1, len(self.portfolio.positions))
        self.assertEqual(890, self.portfolio.money)
        pos = self.portfolio.positions[0]
        self.assertEqual(105, pos.pos_value)
        self.portfolio.compute_liquid_value()
        self.assertEqual(989.75, self.portfolio.liquidative_value)

    def test_sell_two(self):
        self.portfolio.make_operation(Side.SELL, 2, self.transaction_fee)
        self.assertEqual(1, len(self.portfolio.positions))
        self.assertEqual(785, self.portfolio.money)
        pos = self.portfolio.positions[0]
        self.assertEqual(210, pos.pos_value)
        self.portfolio.compute_liquid_value()
        self.assertEqual(984.5, self.portfolio.liquidative_value)

    def test_liquidative_value_with_pos(self):
        p1 = Position(
            side = Side.BUY,
            qty=1,
            pos_value=100
        )
        p2 = Position(
            side = Side.BUY,
            qty=1,
            pos_value=90
        )
        p3 = Position(
            side = Side.SELL,
            qty=1,
            pos_value=80
        )
        self.portfolio.positions.append(p1)
        self.portfolio.positions.append(p2)
        self.portfolio.positions.append(p3)
        self.portfolio.compute_liquid_value()
        self.assertEqual(1275.5, self.portfolio.liquidative_value)

    def test_liquidative_value_no_pos(self):
        self.portfolio.compute_liquid_value()
        self.assertEqual(1000, self.portfolio.liquidative_value)

    def test_close_position_take_profit(self):
        p1 = Position(
            side = Side.BUY,
            qty=1,
            pos_value=100,
            take_profit=0.04,
            stop_loss=-0.05
        )
        p2 = Position(
            side = Side.BUY,
            qty=1,
            pos_value=90,
            take_profit=0.06,
            stop_loss=-0.05
        )
        p3 = Position(
            side = Side.SELL,
            qty=1,
            pos_value=80,
            take_profit=0.04,
            stop_loss=-0.03
        )
        self.portfolio.positions.append(p1)
        self.portfolio.positions.append(p2)
        self.portfolio.positions.append(p3)
        self.portfolio.compute_liquid_value()
        self.assertEqual(1275.5, self.portfolio.liquidative_value)
        self.portfolio.close_position()
        self.assertEqual(1, len(self.portfolio.positions))
        pos = self.portfolio.positions[0]
        self.assertEqual(0.06, pos.take_profit)
        self.assertEqual(1275.5, self.portfolio.liquidative_value)

    def test_close_position_stop_loss(self):
        self.portfolio.asset_perf = -0.04
        p1 = Position(
            side = Side.BUY,
            qty=1,
            pos_value=100,
            take_profit=0.04,
            stop_loss=-0.05
        )
        p2 = Position(
            side = Side.BUY,
            qty=1,
            pos_value=90,
            take_profit=0.06,
            stop_loss=-0.05
        )
        p3 = Position(
            side = Side.SELL,
            qty=1,
            pos_value=80,
            take_profit=0.04,
            stop_loss=-0.03
        )
        self.portfolio.positions.append(p1)
        self.portfolio.positions.append(p2)
        self.portfolio.positions.append(p3)
        self.portfolio.compute_liquid_value()
        self.portfolio.close_position()
        self.assertEqual(2, len(self.portfolio.positions))


if __name__ == '__main__':
    unittest.main(verbosity=2)
