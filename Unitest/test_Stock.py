from unittest import TestCase
import unittest
import Stock
import stock_api_exceptions


class TestStock(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__init__(self):
        #         case where no ticker is inserted
        try:
            stock = Stock.Stock(ticker='')
        except Exception as e:
            self.assertIsInstance(obj=e, cls=stock_api_exceptions.UnknownSymbolException)

    def test__init__2(self):
        #         case where wrong ticker is inserted
        try:
            stock = Stock.Stock(ticker='dfsfsdfsdsfdsf')
        except Exception as e:
            self.assertIsInstance(obj=e, cls=stock_api_exceptions.UnknownSymbolException)

    def test__init__3(self):
        #         case where no internet is available
        try:
            stock = Stock.Stock(ticker='AMZN')
        except Exception as e:
            self.assertIsInstance(obj=e, cls=stock_api_exceptions.ConnectionError)



