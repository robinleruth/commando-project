import unittest

import datetime as dt

from app.domain.model.position import Position
from app.domain.model.side import Side


class TestPosition(unittest.TestCase):
    def setUp(self):
        self.position = Position(
            qty=1,
            pos_value=100,
        )
        print()

    def tearDown(self):
        pass

    def test_compute_pos_value_buy(self):
        perf = 0.05
        self.position.side = Side.BUY
        self.position.compute_pos_value(perf)
        self.assertEqual(105, self.position.pos_value)

    def test_compute_pos_value_double_qty_buy(self):
        perf = 0.05
        self.position.side = Side.BUY
        self.position.qty *= 2
        self.position.pos_value *= 2
        self.position.compute_pos_value(perf)
        self.assertEqual(210, self.position.pos_value)

    def test_compute_pos_value_sell(self):
        perf = 0.05
        self.position.side = Side.SELL
        self.position.compute_pos_value(perf)
        self.assertEqual(95, self.position.pos_value)

    def test_compute_pos_value_double_qty_sell(self):
        perf = 0.05
        self.position.side = Side.SELL
        self.position.qty *= 2
        self.position.pos_value *= 2
        self.position.compute_pos_value(perf)
        self.assertEqual(190, self.position.pos_value)

    def test_compute_pos_value_sell_neg(self):
        perf = -0.05
        self.position.side = Side.SELL
        self.position.compute_pos_value(perf)
        self.assertEqual(105, self.position.pos_value)

    def test_not_take_profit(self):
        perf = 0.04
        self.position.take_profit = 0.05
        self.position.side = Side.BUY
        self.position.compute_pos_value(perf)
        self.assertEqual(False, self.position.close_position)

    def test_not_stop_loss(self):
        perf = -0.04
        self.position.stop_loss = -0.05
        self.position.side = Side.BUY
        self.position.compute_pos_value(perf)
        self.assertEqual(False, self.position.close_position)

    def test_take_profit(self):
        perf = 0.06
        self.position.take_profit = 0.05
        self.position.side = Side.BUY
        self.position.compute_pos_value(perf)
        self.assertEqual(True, self.position.close_position)

    def test_stop_loss(self):
        perf = -0.06
        self.position.stop_loss = -0.05
        self.position.side = Side.BUY
        self.position.compute_pos_value(perf)
        self.assertEqual(True, self.position.close_position)


if __name__ == '__main__':
    unittest.main(verbosity=2)
