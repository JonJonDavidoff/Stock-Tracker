import requests
import json
import Market
import stock_api_exceptions
import datetime
import DbApi
import collections

api_key = "pk_e4cd3161272b47369625df7d517b8714"

market = Market.Market()


class Stock:
    def __init__(self, ticker, amount_of_stocks=0, cost=-1, purchase_date="False"):
        self._amount_of_stocks = int(amount_of_stocks)
        self._ticker = str(ticker)
        self._cost = int(cost)
        if purchase_date == 'False':
            self._purchase_date = '-'
        else:
            self._purchase_date = str(purchase_date)
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
            self._daily_change_money = api['change']
            if cost == -1 or self._amount_of_stocks == -1:  # if stock not purchased
                self._amount_of_stocks = '-'
                self._cost = '-'
                self._stock_holdings = '-'
                self._total_change_money = '-'
            else:
                self._stock_holdings = self._amount_of_stocks * self._price  # current stock holding
                self._total_change_money = (self._price * self._amount_of_stocks) - (
                        self._cost * self._amount_of_stocks)
            #     Get Logo
            api_request = requests.get(
                "https://cloud.iexapis.com/stable/stock/" + self._ticker + "/logo?token=" + api_key)
            self.check_response_code(api_request)
            self._logo = json.loads(api_request.content)['url']

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
        if self._cost == '-' or self._amount_of_stocks == '-':
            return '-'
        return self._cost * self._amount_of_stocks

    def get_stock_gain(self):
        orignal_holdings = self.get_orignal_holdings()
        if self._stock_holdings == '-' or orignal_holdings == '-':
            return '-'
        return self.calculate_percentage_change(current=self._stock_holdings, previous=orignal_holdings)

    def get_company_name(self):
        return self._company_name

    def __str__(self):
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

    def get_historical_data(self, time_range='1d', interval='5'):
        """
        get_historical_data is a function that gets a stock historical data in a certain time range
        :parm time_range: time range is the range of time you would like to get data for. avilable time ranges:
         1d , 5d, 1m, 3m, 6m,ytd, 1y, 5y, max
        """
        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/" + self._ticker + "/chart/" +
            time_range + "/?token=" + api_key + "&chartInterval=" + interval)
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

    def convert_main_stock_data_to_json(self):
        json_dict = {'ticker': self._ticker, 'price': self._price, 'cost': self._cost,
                     'amount_of_stocks': self._amount_of_stocks, 'close_price': self._close_price,
                     'company_name': self._company_name, 'stock_holdings': self._stock_holdings,
                     'daily_change': self._daily_change, 'total_change': self.get_stock_gain(),
                     'daily_change_money': self._daily_change_money, 'total_change_money': self._total_change_money}
        if self._purchase_date != False:
            self._purchase_date = self._purchase_date
        json_dict['purchase_date'] = str(self._purchase_date)
        return json_dict


# U9fFytnoterFaZrPfW1SYLHo8LQL
def average(lst):
    try:
        return sum(lst) / len(lst)
    except:
        return None


def get_list_of_labels(stock, time_range='1d', interval='25'):
    temp_stock_data = None
    list_of_labels = []
    for stock_data in stock.get_historical_data(time_range=time_range, interval=interval):
        list_of_labels.append(stock_data['time'])
    return list_of_labels


def get_list_of_historical_data(list_of_stocks, time_range='1d', interval='25'):
    list_of_historical_data = []
    for stock in list_of_stocks:
        list_of_historical_data.append(stock.get_historical_data(time_range=time_range, interval=interval))
    return list_of_historical_data


def get_list_of_divided_stock_data(list_of_labels, list_of_historical_data):
    list_of_divided_stock_data = collections.defaultdict(list)
    for label in list_of_labels:
        for index in range(len(list_of_historical_data)):
            for stock_data in list_of_historical_data[index]:
                if stock_data['time'] == label and stock_data['price']:
                    list_of_divided_stock_data[label].append(stock_data['price'])
    return list_of_divided_stock_data


def get_list_of_stocks_divided_by_time(time_range='1', interval='25', user_id=1):
    list_of_stocks = DbApi.get_users_stocks_by_user_id(user_id=user_id)
    for st in list_of_stocks:
        print(str(st))
    list_of_labels = get_list_of_labels(stock=list_of_stocks[0], interval=interval)
    print(list_of_labels)
    list_of_historical_data = get_list_of_historical_data(list_of_stocks, time_range=time_range, interval=interval)
    print(list_of_historical_data)
    temp_stock_data = None
    list_of_divided_stock_data = get_list_of_divided_stock_data(list_of_labels=list_of_labels,
                                                                list_of_historical_data=list_of_historical_data)
    print(list_of_divided_stock_data)
    return [list_of_labels, list_of_divided_stock_data]


def get_json_of_average_stocks_price_divided_by_time(list_of_divided_stock_data, list_of_labels):
    dict_of_avg = collections.defaultdict(list)
    for label in list_of_labels:
        avg = average(list_of_divided_stock_data.get(label))
        if avg:
            dict_of_avg[str(label)] = round(avg, 2)
        else:
            dict_of_avg[str(label)] = avg
    print(dict_of_avg)
    return json.dumps(dict_of_avg)


def get_average_stocks_price_divided_by_time():
    pass


def main():
    api_request = requests.get(
        "https://cloud.iexapis.com/stable/stock/" + 'FB' + "/logo?token=pk_e4cd3161272b47369625df7d517b8714")
    print(json.loads(api_request.content))


if __name__ == '__main__':
    main()
