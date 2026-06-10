import decimal
from flask.json.provider import DefaultJSONProvider

class StockFlowJSONProvider(DefaultJSONProvider):
    @staticmethod
    def default(obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(StockFlowJSONProvider, StockFlowJSONProvider).default(obj)
