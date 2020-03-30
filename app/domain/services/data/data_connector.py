import pandas as pd

from abc import ABCMeta
from abc import abstractmethod


class DataConnector(metaclass=ABCMeta):
    @abstractmethod
    def get_df(self) -> pd.DataFrame:
        ''' DF should have Open High Low Close Turnover Volatility '''
        pass
