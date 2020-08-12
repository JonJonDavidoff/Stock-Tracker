import requests
import json
import Market

api_key = "pk_e4cd3161272b47369625df7d517b8714"


market = Market.Market()


class Stock:
    def __init__(self, ticker, amount_of_stocks=0, cost=0):

        self._ticker = ticker
        # TODO Handle Exception
        try:
            api_request = requests.get(
                "https://cloud.iexapis.com/stable/stock/" + self._ticker + "/quote?token=" + api_key)
            api = json.loads(api_request.content)

            self._company_name = api['companyName']
            self._price = api['latestPrice']
            self._close_price = self.get_updated_close_price(api)
            self._daily_change = self.calculate_percentage_change(current=self._price,
                                                                  previous=self._close_price)
            self._amount_of_stocks = amount_of_stocks
            if cost == 0:  # if stock not purchased
                self._cost = self._price
            else:
                self._cost = cost
            self._stock_holdings = self._amount_of_stocks * self._price  # current stock holding

        except Exception as e:
            api = "Error...  "
            print(api + str(e))

    def get_ticker(self):
        return self._ticker

    def get_price(self):
        return self._price

    def get_daily_change(self):
        return self._daily_change

    def get_amount_of_stocks(self):
        return self._amount_of_stocks

    def get_cost(self):
        return self._cost

    def get_close_price(self):
        return self._close_price

    def get_holdings(self):
        return self._stock_holdings

    def get_orignal_holdings(self):
        return self._cost * self._amount_of_stocks

    def get_stock_gain(self):
        return self.calculate_percentage_change(current=self._stock_holdings, previous=self.get_orignal_holdings())

    def get_company_name(self):
        return self._company_name

    def __str__(self):
        return "Stock[ticker=" + self._ticker + ", amount_of_stocks= " + str(self._amount_of_stocks) + ", cost= " + str(
            self._cost) + ", close_price= " + str(self._close_price) + ", price=" + str(
            self._price) + ", daily_change= " + str(round(self._daily_change, 4)) + "%,stock_holdings= " + str(
            self._stock_holdings) + ",orignal_holdings= " + str(self.get_orignal_holdings()) + ", stock_gain= " + str(
            self.get_stock_gain()) + "%, company_name= " + self._company_name + " ]"

    def calculate_percentage_change(self, current, previous):
        """
        calculate_percentage_change is a function that calculates the difference in percentge between two numbers
        :param current:
        :param previous:
        :return:
        """
        if current == previous:
            return 0
        try:
            return ((current - previous) / previous) * 100
        except ZeroDivisionError:
            return float('inf')

    def get_updated_close_price(self, api):
        """
        get_updated_close_price is a function that gets an api and returns the updated_close_price for the Stock
        :param api: api data after call
        :return: Stock correct close price
        """
        close_price = -1
        if market.is_open():
            close_price = api['previousClose']
        else:
            close_price = api['latestPrice']
        return close_price


def main():
    # api_request = requests.get(
    #     "https://cloud.iexapis.com/stable/stock/" + "AMZN" + "/quote?token=" + api_key)
    # api = json.loads(api_request.content)
    # print(api)
    api_request = requests.get(
        "https://cloud.iexapis.com/stable/stock/" + "AMZN" + "/chart/3m?token=" + api_key)

    api = json.loads(api_request.content)
    print(api)


if __name__ == '__main__':
    main()
