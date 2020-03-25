import pandas as pd

from dataclasses import dataclass
from dataclasses import field
from datetime import date

from app.domain.services.data.data_connector import DataConnector
from app.domain.services.data.NoDataFoundException import NoDataFoundException
from app.infrastructure.data.data_connector_factory import data_connector_factory
from app.infrastructure.log import logger
from app.infrastructure.config import app_config


@dataclass
class DataService:
    connector: DataConnector = field(default_factory=data_connector_factory)
    start_date: date = None
    end_date: date = None
    _df: pd.DataFrame = None

    @property
    def df(self):
        if self._df is None:
            logger.info('DataService get data...')
            self._df = self.connector.get_df()
            self._df = self._df.set_index(app_config.AS_OF_DATE).loc[self.start_date:self.end_date].reset_index()
            if self._df.empty:
                raise NoDataFoundException(f'DataFrame is empty for dates {self.start_date} - {self.end_date}')
        return self._df
