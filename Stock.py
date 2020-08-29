import requests
import json
import Market
import stock_api_exceptions
import datetime

api_key = "pk_e4cd3161272b47369625df7d517b8714"

market = Market.Market()


class Stock:
    def __init__(self, ticker, amount_of_stocks=0, cost=0, purchase_date="False"):
        self._amount_of_stocks = amount_of_stocks
        self._ticker = ticker
        self._cost = cost
        if purchase_date != 'False':
            purchase_date = datetime.date(year=int(purchase_date[0:4]), month=int(purchase_date[5:7]), day=int(purchase_date[8:10]))
        self._purchase_date = purchase_date
        # TODO Handle Exception
        try:
            api_request = requests.get(
                "https://cloud.iexapis.com/stable/stock/" + self._ticker + "/quote?token=" + api_key)
            self.check_response_code(api_request)
            api = json.loads(api_request.content)
            self._company_name = api['companyName']
            self._price = api['latestPrice']
            self._close_price = self.get_updated_close_price(api)
            self._daily_change = self.calculate_percentage_change(current=self._price,
                                                                  previous=self._close_price)
            if cost == 0:  # if stock not purchased
                self._cost = self._price
            self._stock_holdings = self._amount_of_stocks * self._price  # current stock holding
        except stock_api_exceptions.UnknownSymbolException as e:
            print(str(e))
        except stock_api_exceptions.ServerErrorException as e:
            print(str(e))
        except Exception as e:
            print(str(e))

    def check_response_code(self, response):
        response_code = int(str(response)[11:14])
        if response_code != 200:
            if response_code == 404:
                raise stock_api_exceptions.UnknownSymbolException
            elif response_code == 500:
                raise stock_api_exceptions.ServerErrorException

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
        print(self._amount_of_stocks)
        return "Stock[ticker=" + self._ticker + ", amount_of_stocks= " + str(self._amount_of_stocks) + ", cost= " + str(
            self._cost) + ", close_price= " + str(self._close_price) + ", price=" + str(
            self._price) + ", daily_change= " + str(round(self._daily_change, 4)) + "%,stock_holdings= " + str(
            self._stock_holdings) + ",orignal_holdings= " + str(self.get_orignal_holdings()) + ", stock_gain= " + str(
            self.get_stock_gain()) + "%, company_name= " + self._company_name + " purchase_date=" + str(
            self._purchase_date) + " ]"

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

    def update_stock_data(self):
        try:
            api_request = requests.get(
                "https://cloud.iexapis.com/stable/stock/" + self._ticker + "/quote?token=" + api_key)
            api = json.loads(api_request.content)

            self._company_name = api['companyName']
            self._price = api['latestPrice']
            self._close_price = self.get_updated_close_price(api)
            self._daily_change = self.calculate_percentage_change(current=self._price,
                                                                  previous=self._close_price)
        except Exception as e:
            api = "Error...  "
            print(api + str(e))

    def get_historical_data(self, time_range):
        """
        get_historical_data is a function that gets a stock historical data in a certain time range
        :parm time_range: time range is the range of time you would like to get data for. avilable time ranges:
         1d , 5d, 1m, 3m, 6m,ytd, 1y, 5y, max
        """
        try:
            api_request = requests.get(
                "https://cloud.iexapis.com/stable/stock/" + self._ticker + "/chart/" + time_range + "?token=" + api_key)
            api_historical_data = json.loads(api_request.content)
            api_data_dict = []
            if time_range != '1d':
                for stock_data in api_historical_data:
                    api_data_dict.append({'price': stock_data['close'], 'time': stock_data['label']})
                print(api_data_dict)
            else:
                for stock_data in api_historical_data:
                    api_data_dict.append({'price': stock_data['average'], 'time': stock_data['label']})
            return api_data_dict
        except Exception as e:
            print(str(e))


# U9fFytnoterFaZrPfW1SYLHo8LQL
def main():
    pass


if __name__ == '__main__':
    main()
