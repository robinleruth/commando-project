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
        df = pd.DataFrame(list(zip(dates, spot)), columns=[app_config.AS_OF_DATE, app_config.SPOT])
        return df
