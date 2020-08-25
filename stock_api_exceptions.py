class UnknownSymbolException(Exception):
    def __init__(self, ticker):
        self._ticker = ticker

    def __str__(self):
        return "Unknown ticker provided " + self._ticker
