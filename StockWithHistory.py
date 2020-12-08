import json
from typing import Any

import requests
import stock_api_exceptions
import Market
import Stock
import threading

api_key = "pk_e4cd3161272b47369625df7d517b8714"

market = Market.Market()
api_url = "https://cloud.iexapis.com/"


class StockWithHistory(Stock.Stock):

    def __init__(self, ticker, amount_of_stocks=0, cost=-1, purchase_date="False"):
        super(StockWithHistory, self).__init__(ticker, amount_of_stocks, cost, purchase_date)
        self._max_historical_data = None
        self._5y_historical_data = None
        self._1y_historical_data = None
        th_max_data = threading.Thread(target=self.get_max_historical_data)
        th_5y_data = threading.Thread(target=self.get_5y_historical_data)
        th_1y_data = threading.Thread(target=self.get_1y_historical_data)
        th_ytd_data = threading.Thread(target=self.get_ytd_historical_data)
        th_6m_data = threading.Thread(target=self.get_six_month_historical_data)
        th_3m_data = threading.Thread(target=self.get_three_month_historical_data)
        th_5d_data = threading.Thread(target=self.get_five_day_historical_data)
        th_1d_data = threading.Thread(target=self.get_one_day_historical_data)
        th_max_data.start()
        th_5y_data.start()
        th_1y_data.start()
        th_ytd_data.start()
        th_6m_data.start()
        th_3m_data.start()
        th_5d_data.start()
        th_1d_data.start()
        th_max_data.join()
        th_5y_data.join()
        th_1y_data.join()
        th_ytd_data.join()
        th_6m_data.join()
        th_3m_data.join()
        th_5d_data.join()
        th_1d_data.join()

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def get_one_day_historical_data(self):
        try:
            api_request = requests.get(
                api_url + "stable/stock/" + self.get_ticker() + "/intraday-prices?token=" + api_key)
        except requests.ConnectionError as e:
            raise stock_api_exceptions.ConnectionError
        self.check_response_code(api_request, self.get_ticker())
        api = json.loads(api_request.content)
        dict_of_labels_and_prices = {'09:30 AM': None, '09:31 AM': None, '09:32 AM': None, '09:33 AM': None,
                                     '09:34 AM': None,
                                     '09:35 AM': None, '09:36 AM': None, '09:37 AM': None, '09:38 AM': None,
                                     '09:39 AM': None,
                                     '09:40 AM': None, '09:41 AM': None, '09:42 AM': None, '09:43 AM': None,
                                     '09:44 AM': None,
                                     '09:45 AM': None, '09:46 AM': None, '09:47 AM': None, '09:48 AM': None,
                                     '09:49 AM': None,
                                     '09:50 AM': None, '09:51 AM': None, '09:52 AM': None, '09:53 AM': None,
                                     '09:54 AM': None,
                                     '09:55 AM': None, '09:56 AM': None, '09:57 AM': None, '09:58 AM': None,
                                     '09:59 AM': None,
                                     '10 AM': None, '10:01 AM': None, '10:02 AM': None, '10:03 AM': None,
                                     '10:04 AM': None,
                                     '10:05 AM': None, '10:06 AM': None, '10:07 AM': None, '10:08 AM': None,
                                     '10:09 AM': None,
                                     '10:10 AM': None, '10:11 AM': None, '10:12 AM': None, '10:13 AM': None,
                                     '10:14 AM': None,
                                     '10:15 AM': None, '10:16 AM': None, '10:17 AM': None, '10:18 AM': None,
                                     '10:19 AM': None,
                                     '10:20 AM': None, '10:21 AM': None, '10:22 AM': None, '10:23 AM': None,
                                     '10:24 AM': None,
                                     '10:25 AM': None, '10:26 AM': None, '10:27 AM': None, '10:28 AM': None,
                                     '10:29 AM': None,
                                     '10:30 AM': None, '10:31 AM': None, '10:32 AM': None, '10:33 AM': None,
                                     '10:34 AM': None,
                                     '10:35 AM': None, '10:36 AM': None, '10:37 AM': None, '10:38 AM': None,
                                     '10:39 AM': None,
                                     '10:40 AM': None, '10:41 AM': None, '10:42 AM': None, '10:43 AM': None,
                                     '10:44 AM': None,
                                     '10:45 AM': None, '10:46 AM': None, '10:47 AM': None, '10:48 AM': None,
                                     '10:49 AM': None,
                                     '10:50 AM': None, '10:51 AM': None, '10:52 AM': None, '10:53 AM': None,
                                     '10:54 AM': None,
                                     '10:55 AM': None, '10:56 AM': None, '10:57 AM': None, '10:58 AM': None,
                                     '10:59 AM': None,
                                     '11 AM': None, '11:01 AM': None, '11:02 AM': None, '11:03 AM': None,
                                     '11:04 AM': None,
                                     '11:05 AM': None, '11:06 AM': None, '11:07 AM': None, '11:08 AM': None,
                                     '11:09 AM': None,
                                     '11:10 AM': None, '11:11 AM': None, '11:12 AM': None, '11:13 AM': None,
                                     '11:14 AM': None,
                                     '11:15 AM': None, '11:16 AM': None, '11:17 AM': None, '11:18 AM': None,
                                     '11:19 AM': None,
                                     '11:20 AM': None, '11:21 AM': None, '11:22 AM': None, '11:23 AM': None,
                                     '11:24 AM': None,
                                     '11:25 AM': None, '11:26 AM': None, '11:27 AM': None, '11:28 AM': None,
                                     '11:29 AM': None,
                                     '11:30 AM': None, '11:31 AM': None, '11:32 AM': None, '11:33 AM': None,
                                     '11:34 AM': None,
                                     '11:35 AM': None, '11:36 AM': None, '11:37 AM': None, '11:38 AM': None,
                                     '11:39 AM': None,
                                     '11:40 AM': None, '11:41 AM': None, '11:42 AM': None, '11:43 AM': None,
                                     '11:44 AM': None,
                                     '11:45 AM': None, '11:46 AM': None, '11:47 AM': None, '11:48 AM': None,
                                     '11:49 AM': None,
                                     '11:50 AM': None, '11:51 AM': None, '11:52 AM': None, '11:53 AM': None,
                                     '11:54 AM': None,
                                     '11:55 AM': None, '11:56 AM': None, '11:57 AM': None, '11:58 AM': None,
                                     '11:59 AM': None,
                                     '12 PM': None, '12:01 PM': None, '12:02 PM': None, '12:03 PM': None,
                                     '12:04 PM': None,
                                     '12:05 PM': None, '12:06 PM': None, '12:07 PM': None, '12:08 PM': None,
                                     '12:09 PM': None,
                                     '12:10 PM': None, '12:11 PM': None, '12:12 PM': None, '12:13 PM': None,
                                     '12:14 PM': None,
                                     '12:15 PM': None, '12:16 PM': None, '12:17 PM': None, '12:18 PM': None,
                                     '12:19 PM': None,
                                     '12:20 PM': None, '12:21 PM': None, '12:22 PM': None, '12:23 PM': None,
                                     '12:24 PM': None,
                                     '12:25 PM': None, '12:26 PM': None, '12:27 PM': None, '12:28 PM': None,
                                     '12:29 PM': None,
                                     '12:30 PM': None, '12:31 PM': None, '12:32 PM': None, '12:33 PM': None,
                                     '12:34 PM': None,
                                     '12:35 PM': None, '12:36 PM': None, '12:37 PM': None, '12:38 PM': None,
                                     '12:39 PM': None,
                                     '12:40 PM': None, '12:41 PM': None, '12:42 PM': None, '12:43 PM': None,
                                     '12:44 PM': None,
                                     '12:45 PM': None, '12:46 PM': None, '12:47 PM': None, '12:48 PM': None,
                                     '12:49 PM': None,
                                     '12:50 PM': None, '12:51 PM': None, '12:52 PM': None, '12:53 PM': None,
                                     '12:54 PM': None,
                                     '12:55 PM': None, '12:56 PM': None, '12:57 PM': None, '12:58 PM': None,
                                     '12:59 PM': None,
                                     '1 PM': None, '1:01 PM': None, '1:02 PM': None, '1:03 PM': None, '1:04 PM': None,
                                     '1:05 PM': None, '1:06 PM': None, '1:07 PM': None, '1:08 PM': None,
                                     '1:09 PM': None,
                                     '1:10 PM': None, '1:11 PM': None, '1:12 PM': None, '1:13 PM': None,
                                     '1:14 PM': None,
                                     '1:15 PM': None, '1:16 PM': None, '1:17 PM': None, '1:18 PM': None,
                                     '1:19 PM': None,
                                     '1:20 PM': None, '1:21 PM': None, '1:22 PM': None, '1:23 PM': None,
                                     '1:24 PM': None,
                                     '1:25 PM': None, '1:26 PM': None, '1:27 PM': None, '1:28 PM': None,
                                     '1:29 PM': None,
                                     '1:30 PM': None, '1:31 PM': None, '1:32 PM': None, '1:33 PM': None,
                                     '1:34 PM': None,
                                     '1:35 PM': None, '1:36 PM': None, '1:37 PM': None, '1:38 PM': None,
                                     '1:39 PM': None,
                                     '1:40 PM': None, '1:41 PM': None, '1:42 PM': None, '1:43 PM': None,
                                     '1:44 PM': None,
                                     '1:45 PM': None, '1:46 PM': None, '1:47 PM': None, '1:48 PM': None,
                                     '1:49 PM': None,
                                     '1:50 PM': None, '1:51 PM': None, '1:52 PM': None, '1:53 PM': None,
                                     '1:54 PM': None,
                                     '1:55 PM': None, '1:56 PM': None, '1:57 PM': None, '1:58 PM': None,
                                     '1:59 PM': None,
                                     '2 PM': None, '2:01 PM': None, '2:02 PM': None, '2:03 PM': None, '2:04 PM': None,
                                     '2:05 PM': None, '2:06 PM': None, '2:07 PM': None, '2:08 PM': None,
                                     '2:09 PM': None,
                                     '2:10 PM': None, '2:11 PM': None, '2:12 PM': None, '2:13 PM': None,
                                     '2:14 PM': None,
                                     '2:15 PM': None, '2:16 PM': None, '2:17 PM': None, '2:18 PM': None,
                                     '2:19 PM': None,
                                     '2:20 PM': None, '2:21 PM': None, '2:22 PM': None, '2:23 PM': None,
                                     '2:24 PM': None,
                                     '2:25 PM': None, '2:26 PM': None, '2:27 PM': None, '2:28 PM': None,
                                     '2:29 PM': None,
                                     '2:30 PM': None, '2:31 PM': None, '2:32 PM': None, '2:33 PM': None,
                                     '2:34 PM': None,
                                     '2:35 PM': None, '2:36 PM': None, '2:37 PM': None, '2:38 PM': None,
                                     '2:39 PM': None,
                                     '2:40 PM': None, '2:41 PM': None, '2:42 PM': None, '2:43 PM': None,
                                     '2:44 PM': None,
                                     '2:45 PM': None, '2:46 PM': None, '2:47 PM': None, '2:48 PM': None,
                                     '2:49 PM': None,
                                     '2:50 PM': None, '2:51 PM': None, '2:52 PM': None, '2:53 PM': None,
                                     '2:54 PM': None,
                                     '2:55 PM': None, '2:56 PM': None, '2:57 PM': None, '2:58 PM': None,
                                     '2:59 PM': None,
                                     '3 PM': None, '3:01 PM': None, '3:02 PM': None, '3:03 PM': None, '3:04 PM': None,
                                     '3:05 PM': None, '3:06 PM': None, '3:07 PM': None, '3:08 PM': None,
                                     '3:09 PM': None,
                                     '3:10 PM': None, '3:11 PM': None, '3:12 PM': None, '3:13 PM': None,
                                     '3:14 PM': None,
                                     '3:15 PM': None, '3:16 PM': None, '3:17 PM': None, '3:18 PM': None,
                                     '3:19 PM': None,
                                     '3:20 PM': None, '3:21 PM': None, '3:22 PM': None, '3:23 PM': None,
                                     '3:24 PM': None,
                                     '3:25 PM': None, '3:26 PM': None, '3:27 PM': None, '3:28 PM': None,
                                     '3:29 PM': None,
                                     '3:30 PM': None, '3:31 PM': None, '3:32 PM': None, '3:33 PM': None,
                                     '3:34 PM': None,
                                     '3:35 PM': None, '3:36 PM': None, '3:37 PM': None, '3:38 PM': None,
                                     '3:39 PM': None,
                                     '3:40 PM': None, '3:41 PM': None, '3:42 PM': None, '3:43 PM': None,
                                     '3:44 PM': None,
                                     '3:45 PM': None, '3:46 PM': None, '3:47 PM': None, '3:48 PM': None,
                                     '3:49 PM': None,
                                     '3:50 PM': None, '3:51 PM': None, '3:52 PM': None, '3:53 PM': None,
                                     '3:54 PM': None,
                                     '3:55 PM': None, '3:56 PM': None, '3:57 PM': None, '3:58 PM': None,
                                     '3:59 PM': None}
        for d in api:
            dict_of_labels_and_prices[d['label']] = d['average']
        self._one_day_historical_data = dict_of_labels_and_prices


def main():
    amzn = StockWithHistory(ticker='AMZN')
    print(amzn.get_one_day_historical_data())


if __name__ == '__main__':
    main()
