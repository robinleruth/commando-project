import unittest

from app.domain.services.data.data_service import DataService


class TestDataService(unittest.TestCase):
    def setUp(self):
        self.service = DataService()

    def tearDown(self):
        pass

    def test_get_data(self):
        df = self.service.df


if __name__ == '__main__':
    unittest.main(verbosity=2)
