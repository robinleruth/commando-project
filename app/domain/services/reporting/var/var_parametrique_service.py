import math

from app.domain.services.reporting.var.var_service import VarService


class VarParametriqueService(VarService):
    def __init__(self, vol):
        self.vol = vol

    def get_value_at_risk(self) -> float:
        ''' VaR 1 day 95%'''
        return self.vol / (math.sqrt(252)) * 1.645 # z-score for 95% confidence rate
