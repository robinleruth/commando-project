import random
import pandas as pd
import datetime as dt

from app.domain.services.data.data_connector import DataConnector
from app.infrastructure.config import app_config


class MockDataConnector(DataConnector):
    def get_df(self) -> pd.DataFrame:
        dates = ['2020-03-{}'.format(str(i)) for i in range(1, 31)]
        dates = list(map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d"), dates))
        spot = [random.randint(50, 200) for _ in range(1, 31)]
        high = [random.randint(80, 120) for _ in range(1, 31)]
        low = [round(i * (1 - random.random())) for i in high]
        open = [random.randint(i[1], i[0]) for i in list(zip(high, low))]
        close = [random.randint(i[1], i[0]) for i in list(zip(high, low))]
        vol = [random.randint(80, 120) for _ in range(1, 31)]
        df = pd.DataFrame(list(zip(dates, spot, open, high, low, close, vol)),
                          columns=[app_config.AS_OF_DATE, app_config.SPOT,
                                   app_config.OPEN, app_config.HIGH,
                                   app_config.LOW, app_config.CLOSE,
                                   app_config.VOLATILITY])
        df[app_config.TURNOVER] = 0
        return df
