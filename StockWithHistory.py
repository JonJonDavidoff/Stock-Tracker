import Stock
import threading


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


def main():
    print(StockWithHistory(ticker='AMZN'))


if __name__ == '__main__':
    main()
