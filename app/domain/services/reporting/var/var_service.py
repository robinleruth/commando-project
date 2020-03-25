from abc import ABCMeta
from abc import abstractmethod


class VarService(metaclass=ABCMeta):
    @abstractmethod
    def get_value_at_risk(self):
        pass
