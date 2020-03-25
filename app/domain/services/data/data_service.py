import pandas as pd

from dataclasses import dataclass
from dataclasses import field

from app.domain.services.data.data_connector import DataConnector
from app.infrastructure.data.data_connector_factory import data_connector_factory
from app.infrastructure.log import logger


@dataclass
class DataService:
    connector: DataConnector = field(default_factory=data_connector_factory)
    _df: pd.DataFrame = None

    @property
    def df(self):
        if self._df is None:
            logger.info('DataService get data...')
            self._df = self.connector.get_df()
        return self._df
