from app.domain.services.data.data_connector import DataConnector
from app.infrastructure.data.mock_data_connector import MockDataConnector


def data_connector_factory() -> DataConnector:
    return MockDataConnector()
