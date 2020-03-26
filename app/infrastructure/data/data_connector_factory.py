from app.domain.services.data.data_connector import DataConnector
from app.domain.services.data.available_stocks import AvailableStocks
from app.infrastructure.data.mock_data_connector import MockDataConnector
from app.infrastructure.data.gspc_file_connector import GspcFileConnector


def data_connector_factory(stock: AvailableStocks) -> DataConnector:
    if stock is AvailableStocks.MOCK:
        return MockDataConnector()
    if stock is AvailableStocks.SP500:
        return GspcFileConnector()
    return None
