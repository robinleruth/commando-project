import unittest
import pandas as pd
import datetime as dt

from unittest.mock import MagicMock
from matplotlib.figure import Figure

from app.domain.services.reporting.reporting_service import ReportingService
from app.infrastructure.config import app_config


class TestReportingService(unittest.TestCase):
    def setUp(self):
        dates = ['2020-03-01', '2020-03-02', '2020-03-03', '2020-03-04',
                 '2020-03-05', '2020-03-06']
        dates = list(map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d"), dates))
        spot = [100, 105, 102, 110, 90, 95]
        asset_value = [100, 105, 102, 110, 90, 95]
        df = pd.DataFrame(list(zip(dates, spot, asset_value)),
                          columns=[app_config.AS_OF_DATE, app_config.SPOT, 'asset_value'])
        ptf_service = MagicMock()
        ptf_service.ptf_to_df = MagicMock(return_value=df)
        var_service = MagicMock()
        var_service.get_value_at_risk = MagicMock(return_value=0)
        self.reporting_service = ReportingService(ptf_service=ptf_service,
                                                  var_service=var_service)
        print()

    def tearDown(self):
        pass

    def test_max_draw_down(self):
        self.reporting_service.compute_max_draw_down()
        self.assertAlmostEqual(-0.18, self.reporting_service.max_draw_down, 2)

    def test_vol(self):
        self.reporting_service.compute_vol()
        self.assertAlmostEqual(1.69, self.reporting_service.vol_annu, 2)

    def test_perf_annu(self):
        self.reporting_service.compute_perf_annu()
        self.assertAlmostEqual(-0.956, self.reporting_service.perf_annu, 3)

    def test_sharpe_ratio(self):
        self.reporting_service.compute_sharpe_ratio()
        self.assertAlmostEqual(-0.565, self.reporting_service.sharpe_ratio, 3)

    def test_base_100(self):
        b = self.reporting_service.compute_base_100()
        self.assertAlmostEqual(97.36, b['base_100'].iloc[-1], 2)

    def test_graph(self):
        fig: Figure = self.reporting_service.generate_graph()
        fig.savefig('test.png')

    def test_var(self):
        var = self.reporting_service.compute_var()
        self.assertAlmostEqual(0.18, var, 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
