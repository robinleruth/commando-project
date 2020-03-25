import pandas as pd

from abc import ABCMeta
from abc import abstractmethod
from datetime import date


class DataConnector(metaclass=ABCMeta):
    @abstractmethod
    def get_df(self, start_date: date=None, end_date: date=None) -> pd.DataFrame:
        pass
