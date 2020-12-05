class UnknownSymbolException(Exception):
    def __init__(self, ticker):
        self._ticker = ticker

    def __str__(self):
        return "Unknown ticker provided " + self._ticker


class ServerErrorException(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "An Error with the stock System has occurred please try again"


