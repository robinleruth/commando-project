import random
import pandas as pd
import datetime as dt

from app.domain.services.data.data_connector import DataConnector
from app.infrastructure.config import app_config


class MockDataConnector(DataConnector):
    def get_df(self) -> pd.DataFrame:
        dates = ['2020-03-{}'.format(str(i)) for i in range(1, 31)]
        dates = list(map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d"), dates))
        spot = [random.randint(80, 120) for _ in range(1, 31)]
        open = [random.randint(80, 120) for _ in range(1, 31)]
        high = [random.randint(80, 120) for _ in range(1, 31)]
        close = [random.randint(80, 120) for _ in range(1, 31)]
        low = [random.randint(80, 120) for _ in range(1, 31)]
        vol = [random.randint(80, 120) for _ in range(1, 31)]
        df = pd.DataFrame(list(zip(dates, spot, open, high, low, close, vol)),
                          columns=[app_config.AS_OF_DATE, app_config.SPOT,
                                   app_config.OPEN, app_config.HIGH,
                                   app_config.LOW, app_config.CLOSE,
                                   app_config.VOLATILITY])
        df[app_config.TURNOVER] = 0
        return df
