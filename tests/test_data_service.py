import unittest
import pandas as pd

from unittest.mock import MagicMock

from app.domain.services.data.data_service import DataService


class TestDataService(unittest.TestCase):
    def setUp(self):
        data_connector = MagicMock()
        data_connector.get_df = MagicMock(return_value=pd.DataFrame())
        self.service = DataService(data_connector)

    def tearDown(self):
        pass

    def test_get_data(self):
        df = self.service.df


if __name__ == '__main__':
    unittest.main(verbosity=2)
