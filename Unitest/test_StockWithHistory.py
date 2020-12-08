from unittest import TestCase
import StockWithHistory
import stock_api_exceptions


class TestStockWithHistory(TestCase):
    def test__init__(self):
        #         case where no internet is available
        try:
            stock = StockWithHistory.StockWithHistory(ticker='AMZN')
        except Exception as e:
            self.assertIsInstance(obj=e, cls=stock_api_exceptions.ConnectionError)

    def test_get_one_day_historical_data(self):
        # positive case
        stock = StockWithHistory.StockWithHistory(ticker='twtr')
        self.assertIsInstance(obj=stock._one_day_historical_data, cls=dict)

    def test__init__unknown_ticker(self):
        try:
            stock = StockWithHistory.StockWithHistory(ticker='sdffdsfds')
        except Exception as e:
            self.assertIsInstance(obj=e, cls=stock_api_exceptions.UnknownSymbolException)

    def tearDown(self) -> None:
        pass
