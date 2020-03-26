import os
import pandas as pd

from app.domain.services.data.data_connector import DataConnector
from app.infrastructure.config import app_config


class GspcFileConnector(DataConnector):
    def get_df(self) -> pd.DataFrame:
        file_path = os.path.abspath(os.path.dirname(__file__))
        df = pd.read_csv(os.path.join(file_path, 'sp500.csv'))
        df[app_config.AS_OF_DATE] = pd.to_datetime(df[app_config.AS_OF_DATE])
        return df
