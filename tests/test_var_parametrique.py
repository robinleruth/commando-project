import unittest

from app.domain.services.reporting.var.var_parametrique_service import VarParametriqueService


class TestVarParametrique(unittest.TestCase):
    def setUp(self):
        self.var_service = VarParametriqueService(0.10)
        print()

    def tearDown(self):
        pass

    def test_var(self):
        self.assertAlmostEqual(0.0103, self.var_service.get_value_at_risk(), 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
