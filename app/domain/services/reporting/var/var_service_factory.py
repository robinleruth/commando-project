from app.domain.services.reporting.var.var_service import VarService
from app.domain.services.reporting.var.var_parametrique_service import VarParametriqueService


def var_service_factory() -> VarService:
    return VarParametriqueService(0.05)
