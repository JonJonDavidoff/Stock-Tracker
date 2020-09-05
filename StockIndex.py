from __future__ import print_function
import time
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException

intrinio.ApiClient().configuration.api_key['api_key'] = 'OjUwYjk1NjVhZTY4YWFmODRkOGZmZTAwNmQ2N2ExMzli'




class StockIndex:
    def __init__(self, ticker):
        pass

def main():
    identifier = '^GSPC'
    start_date = '2018-01-01'
    end_date = '2019-01-01'
    frequency = 'daily'
    page_size = 100
    next_page = ''
    response = intrinio.SecurityApi().get_security_stock_prices(identifier, start_date=start_date, end_date=end_date,
                                                                frequency=frequency, page_size=page_size,
                                                                next_page=next_page)
    print(response)

if __name__ == '__main__':
    main()