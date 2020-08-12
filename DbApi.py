import pyodbc
import User
import Stock


class DbApi:
    def __init__(self):
        pass

    def execute_query(self, sql):
        try:
            conn_and_cursor = self.create_conn()
            conn_and_cursor[0].execute(sql)
            conn_and_cursor[0].commit()
            self.close_conn(conn_and_cursor[1])
        except Exception as e:
            print("Error" + str(e))

    def add_user(self, first_name, last_name, email, password):
        """
        add_user is a function that check if the user exists in db and if it doesnt exits adds it to db
        :param first_name:
        :param last_name:
        :param email:
        :param password
        :return: None
        """
        try:
            # TODO Add the check to form instead of here
            if User.check_user(email=email, password=password):
                if not (self.is_exist("SELECT * FROM dbo.Users WHERE Email='" + email + "'")):
                    insert_query = "INSERT INTO dbo.Users (FirstName, LastName , Email, Password) VALUES ('" + first_name + "','" + last_name \
                                   + "','" + email + "', '" + password + "');"
                    self.execute_query(insert_query)
                    print("User added successfully")
                    return True
                else:
                    # TODO create message on ui
                    print("User already exists")
                    return False

        except Exception:
            # TODO Handle Exception properly
            print("Error")

    def is_exist(self, sql):
        """
        is_exist is a function that checks if a user exists in a db
        :return: bool values True if user exists False if it does not
        """
        try:
            data = self.execute_select_query(
                sql=sql)
            if len(data) > 0:
                return True
            else:
                return False
        except Exception:
            print("Error")

    def execute_select_query(self, sql):
        """
        execute_select_query is a funtion that gets an sql select query and returns the requested data
        :param sql: select query
        :return: the requested data
        """
        try:
            conn_and_cursor = self.create_conn()
            conn_and_cursor[0].execute(sql)
            data = conn_and_cursor[0].fetchall()
            conn_and_cursor[0].commit()
            self.close_conn(conn_and_cursor[1])
            return data
        except Exception as e:
            print("Error  " + str(e))

    def create_conn(self, db_name="StockTracker"):
        """
        create_conn is a function that creates a connection between db and python
        :param db_name: the db's name
        :return: tuple of connection and cursor for actions
        """
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-RDOEULV;'
                              'Database=' + db_name + ';'
                                                      'Trusted_Connection=yes;UID=sa;PWD=jonjon1212')
        cursor = conn.cursor()
        return cursor, conn

    def close_conn(self, conn):
        """
        close_conn is a function that closes the connection to the db
        :param conn: the connection
        :return: None
        """
        conn.close()

    #  add_user is a function that check if the user exists in db and if it doesnt exits adds it to db
    def add_stock(self, ticker, user_id, cost_of_stock=-1, amount_of_stocks=0):
        """
        add_stock is a function that checks if the stock exists in the  db and if it doesnt exits adds it to db
        :param ticker:
        :param user_id:
        :param cost_of_stock:
        :param amount_of_stocks:
        :return: None
        """
        try:
            if not (
                    self.is_exist(
                        sql="SELECT * FROM dbo.Stocks WHERE ticker='" + ticker + "'AND user_id=" + str(user_id))):
                insert_query = "INSERT INTO dbo.Stocks (ticker, amount_of_stocks, cost, user_id) " \
                               "VALUES('" + ticker + "'," + str(amount_of_stocks) + "," + str(
                    cost_of_stock) + "," + str(
                    user_id) + ")"
                self.execute_query(insert_query)
                print('The Stock: ' + ticker + ', was added successfully')
                return True
            else:
                # TODO create message on ui
                print("Stock already exists")
                return False
        except Exception:
            print("Error")

    def get_user_id_by_email(self, email):
        """
        get_user_id_by_email is a function that gets an email and retuns the related user id
        :param email: the users email
        :return: the user's id
        """
        return self.get_user_by_email(email).get_id()

    def add_stock_by_email(self, email, ticker, cost_of_stock=-1, amount_of_stocks=0):
        """
         add_stock_by_email is a function that get the user_id  checks if the stock exists in the  db and if it doesnt exits adds it to db
        :param email:
        :param ticker:
        :param cost_of_stock:
        :param amount_of_stocks:
        :return: None
        """
        user = self.get_user_by_email(email)
        self.add_stock(ticker=ticker, user_id=user.get_id(), cost_of_stock=cost_of_stock,
                       amount_of_stocks=amount_of_stocks)

    def get_user_by_email(self, email):
        """
        get_user_by_email is a function that conects to the db and returns the user by the email
        :param email: the email of the user
        :return: User object
        """
        try:
            data = self.execute_select_query(sql="SELECT * FROM dbo.Users WHERE Email='" + email + "'")
            list = self.data_to_list(data)
            user = User.User(user_id=list[0][0], first_name=list[0][1], last_name=list[0][2], email=list[0][3],
                             password=list[0][4])
            return user
        except Exception:
            print("Error")

    def get_user_by_id(self, id):
        try:
            data = self.execute_select_query(sql="SELECT * FROM dbo.Users WHERE id=" + str(id) + "")
            list = self.data_to_list(data)
            user = User.User(user_id=list[0][0], first_name=list[0][1], last_name=list[0][2], email=list[0][3],
                             password=list[0][4])
            return user
        except Exception:
            print("Error")

    def data_to_list(self, data):
        list = []
        for row in data:
            row_to_list = [elem for elem in row]
            list.append(row_to_list)
        return list

    def get_users_stocks_by_user_id(self, user_id):
        """
        get_users_stocks_by_user_id is a function that gets a user id and returns all of the users stocks
        :param user_id: the user id to search for
        :return: list of Stocks
        """
        # get data from db
        stock_data = self.execute_select_query(sql="SELECT * FROM dbo.Stocks WHERE user_id=" + str(user_id))
        # convert data to list
        list_of_stocks = self.data_to_list(stock_data)
        # move data to list of all stocks
        return_user_stocks_list = []
        temp_stock = 0
        for stock in list_of_stocks:
            temp_stock = Stock.Stock(ticker=stock[1], amount_of_stocks=stock[2], cost=stock[4])
            return_user_stocks_list.append(temp_stock)
        return return_user_stocks_list

    def get_users_stock_by_ticker(self, user_id, ticker):
        try:
            sql = "SELECT * FROM dbo.Stocks WHERE ticker='" + ticker + "' AND user_id=" + str(user_id)
            data = self.execute_select_query(sql)
            data = self.data_to_list(data)
            return Stock.Stock(ticker=data[0][1], amount_of_stocks=data[0][2], cost=data[0][4])
        except Exception as e:
            print("Error... " + str(e))

    def get_users_stocks_by_email(self, email):
        """
         get_users_stocks_by_user_id is a function that gets an email and returns all of the users stocks
        :param email:
        :return:
        """
        return self.get_users_stocks_by_user_id(user_id=self.get_user_id_by_email(email))

    def print_all_users(self):
        """
        print_all_users is a function that prints all users from the Users table
        :return: None
        """
        data = self.execute_select_query("SELECT * FROM dbo.Users")
        print("[id   FirstName   LastName   Email                             Password]")
        for row in data:
            print(row)

    def print_all_stocks(self):
        """
        print_all_users is a function that prints all stocks from the Stocks table
        :return: None
        """
        data = self.execute_select_query("SELECT * FROM dbo.Stocks")
        print("[id   ticker   amount_of_stocks   user_id cost]")
        for row in data:
            print(row)

    def remove_stock_by_user_id(self, ticker, user_id):
        """
        remove_stock_by_user_id is a function that removes a stocks by the user's id
        :param ticker: the stocks ticker
        :param user_id: the user's id
        :return: None
        """
        self.execute_query(sql="DELETE FROM dbo.Stocks WHERE ticker='" + ticker + "' AND user_id=" + str(user_id))

    def remove_user(self, user_id):
        """
          remove_stock_by_user_id is a function that removes a user and its stocks from db by the user's id
          :param user_id: the user's id
          :return: None
          """
        self.execute_query(sql="DELETE FROM dbo.Stocks WHERE user_id=" + str(user_id))
        self.execute_query("DELETE FROM dbo.Users WHERE id=" + str(user_id))

    def update_stock(self, ticker, user_id, amount_of_stocks=-1, cost=-1):
        """
        update_stock is a function that gets a ticker, user_id , amount_of_stocks, cost and updates the db accordingly
        if default value,-1, the default will stay the same
        :param ticker:
        :param user_id:
        :param amount_of_stocks: if default will stay the same values from the db
        :param cost: if default will stay the same values from the db
        :return: None
        """
        try:
            if amount_of_stocks == -1 or cost == -1:
                stock = self.get_users_stock_by_ticker(ticker=ticker, user_id=user_id)
                if amount_of_stocks == -1:
                    amount_of_stocks = stock.get_amount_of_stocks()
                else:
                    cost = stock.get_cost()

            self.execute_query(
                "UPDATE dbo.Stocks SET amount_of_stocks =" + str(amount_of_stocks) + " , cost = " + str(
                    cost) + "  WHERE user_id =" + str(user_id) + "  AND ticker = '" + ticker + "'")
        except Exception as e:
            print("Error  " + str(e))


def main():
    pass


if __name__ == '__main__':
    main()
