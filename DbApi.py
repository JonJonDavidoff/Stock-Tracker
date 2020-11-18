import pyodbc
import User
import Stock
import Logger

def execute_query(sql):
    try:
        conn_and_cursor = create_conn()
        conn_and_cursor[0].execute(sql)
        conn_and_cursor[0].commit()
        close_conn(conn_and_cursor[1])
    except Exception as e:
        Logger.Log.get_log().log(file_name='Stock.py', exception=str(e), function_name='update_stock')


def add_user(first_name, last_name, email, password):
    """
    add_user is a function that check if the user exists in db and if it doesnt exits adds it to db
    :param first_name:
    :param last_name:
    :param email:
    :param password
    :return: None
    """
    try:
        if not (is_exist("SELECT * FROM dbo.Users WHERE Email='" + email + "'")):
            insert_query = "INSERT INTO dbo.Users (FirstName, LastName , Email, Password) VALUES ('" + first_name + "','" + last_name \
                           + "','" + email + "', '" + password + "');"
            execute_query(insert_query)
            print("User added successfully")
            return True
        else:
            # TODO create message on ui
            print("User already exists")
            return False

    except Exception:
        # TODO Handle Exception properly
        print("Error")


def is_exist(sql):
    """
    is_exist is a function that checks if a user exists in a db
    :return: bool values True if user exists False if it does not
    """
    try:
        data = execute_select_query(
            sql=sql)
        print(data)
        if len(data) > 0:
            return True
        else:
            return False
    except Exception as e:
        print(str(e))


def execute_select_query(sql):
    """
    execute_select_query is a funtion that gets an sql select query and returns the requested data
    :param sql: select query
    :return: the requested data
    """
    try:
        conn_and_cursor = create_conn()
        conn_and_cursor[0].execute(sql)
        data = conn_and_cursor[0].fetchall()
        conn_and_cursor[0].commit()
        close_conn(conn_and_cursor[1])
        return data
    except Exception as e:
        print("Error  " + str(e))


def create_conn(db_name="StockTracker"):
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


def close_conn(conn):
    """
    close_conn is a function that closes the connection to the db
    :param conn: the connection
    :return: None
    """
    conn.close()


#  add_user is a function that check if the user exists in db and if it doesnt exits adds it to db
def add_stock(ticker, user_id, cost_of_stock=-1, amount_of_stocks=0, purchese_date="False"):
    """
    add_stock is a function that checks if the stock exists in the  db and if it doesnt exits adds it to db
    :param ticker:
    :param user_id:
    :param cost_of_stock:
    :param amount_of_stocks:
    :return: None
    """
    # try:
    if not (
            is_exist(
                sql="SELECT * FROM dbo.Stocks WHERE ticker='" + ticker + "'AND user_id=" + str(user_id))):
        insert_query = "INSERT INTO dbo.Stocks " \
                       "VALUES ('" + str(ticker) + "'," + str(amount_of_stocks) + "," + str(user_id) + "," + str(
            cost_of_stock) + ",'" + str(purchese_date) + "')"
        execute_query(insert_query)
        print('The Stock: ' + ticker + ', was added successfully')
        return True
    else:
        # TODO create message on ui
        print("Stock already exists")
        return False


# except Exception as e:
#     print("Error  " + str(e))


def add_stock_by_email(email, ticker, cost_of_stock=-1, amount_of_stocks=0, purchese_date="False"):
    """
     add_stock_by_email is a function that get the user_id  checks if the stock exists in the  db and if it doesnt exits adds it to db
    :param email:
    :param ticker:
    :param cost_of_stock:
    :param amount_of_stocks:
    :return: None
    """
    print(ticker)
    add_stock(ticker=ticker, user_id=get_user_id_by_email(email), cost_of_stock=cost_of_stock,
              amount_of_stocks=amount_of_stocks, purchese_date=purchese_date)


def get_user_by_email(email):
    """
    get_user_by_email is a function that conects to the db and returns the user by the email
    :param email: the email of the user
    :return: User object
    """
    try:
        data = execute_select_query(sql="SELECT * FROM dbo.Users WHERE Email='" + email + "'")
        list = data_to_list(data)
        user = User.User(user_id=list[0][0], first_name=list[0][1], last_name=list[0][2], email=list[0][3],
                         password=list[0][4])
        return user
    except Exception as e:
        print("Error " + str(e))


def get_user_by_id(id):
    try:
        data = execute_select_query(sql="SELECT * FROM dbo.Users WHERE id=" + str(id) + "")
        list = data_to_list(data)
        user = User.User(user_id=list[0][0], first_name=list[0][1], last_name=list[0][2], email=list[0][3],
                         password=list[0][4])
        return user
    except Exception:
        print("Error")


def data_to_list(data):
    list = []
    for row in data:
        row_to_list = [elem for elem in row]
        list.append(row_to_list)
    return list


def get_users_stocks_by_user_id(user_id):
    """
    get_users_stocks_by_user_id is a function that gets a user id and returns all of the users stocks
    :param user_id: the user id to search for
    :return: list of Stocks
    """
    # get data from db
    stock_data = execute_select_query(sql="SELECT * FROM dbo.Stocks WHERE user_id=" + str(user_id))
    # convert data to list
    list_of_stocks = data_to_list(stock_data)
    # move data to list of all stocks
    return_user_stocks_list = []
    temp_stock = 0
    for stock in list_of_stocks:
        temp_stock = Stock.Stock(ticker=stock[1], amount_of_stocks=stock[2], cost=stock[4], purchase_date=stock[5])
        return_user_stocks_list.append(temp_stock)
    return return_user_stocks_list


def get_users_stock_by_ticker(user_id, ticker):
    sql = "SELECT * FROM dbo.Stocks WHERE ticker='" + ticker + "' AND user_id=" + str(user_id)
    data = execute_select_query(sql)
    data = data_to_list(data)
    print(data)
    return Stock.Stock(ticker=data[0][1], amount_of_stocks=data[0][2], cost=data[0][4], purchase_date=data[0][5])

    # print("Error... " + str(e))


def get_users_stocks_by_email(email):
    """
     get_users_stocks_by_user_id is a function that gets an email and returns all of the users stocks
    :param email:
    :return:
    """
    return get_users_stocks_by_user_id(user_id=get_user_id_by_email(email))


def print_all_users():
    """
    print_all_users is a function that prints all users from the Users table
    :return: None
    """
    data = execute_select_query("SELECT * FROM dbo.Users")
    print("[id   FirstName   LastName   Email                             Password]")
    for row in data:
        print(row)


def print_all_stocks():
    """
    print_all_users is a function that prints all stocks from the Stocks table
    :return: None
    """
    data = execute_select_query("SELECT * FROM dbo.Stocks")
    print("[id   ticker   amount_of_stocks   user_id cost]")
    for row in data:
        print(row)


def remove_stock_by_user_id(ticker, user_id):
    """
    remove_stock_by_user_id is a function that removes a stocks by the user's id
    :param ticker: the stocks ticker
    :param user_id: the user's id
    :return: None
    """
    execute_query(sql="DELETE FROM dbo.Stocks WHERE ticker='" + ticker + "' AND user_id=" + str(user_id))


def stock_by_email(email, tick):
    pass


def remove_user_by_user_id(user_id):
    """
      remove_stock_by_user_id is a function that removes a user and its stocks from db by the user's id
      :param user_id: the user's id
      :return: None
      """
    execute_query(sql="DELETE FROM dbo.Stocks WHERE user_id=" + str(user_id))
    execute_query("DELETE FROM dbo.Users WHERE id=" + str(user_id))


def get_user_id_by_email(email):
    """
    get_user_id_by_email is a function that gets an email and retuns the related user id
    :param email: the users email
    :return: the user's id
    """
    usr = get_user_by_email(email)
    return usr.user_id


def get_user_by_email(email):
    """
    get_user_by_email is a function that conects to the db and returns the user by the email
    :param email: the email of the user
    :return: User object
    """
    try:
        data = execute_select_query(sql="SELECT * FROM dbo.Users WHERE Email='" + email + "'")
        list = data_to_list(data)
        user = User.User(user_id=list[0][0], first_name=list[0][1], last_name=list[0][2], email=list[0][3],
                         password=list[0][4])
        return user
    except Exception:
        print("Error")


def get_user_by_id(id):
    try:
        data = execute_select_query(sql="SELECT * FROM dbo.Users WHERE id=" + str(id) + "")
        list = data_to_list(data)
        user = User.User(user_id=list[0][0], first_name=list[0][1], last_name=list[0][2], email=list[0][3],
                         password=list[0][4])
        return user
    except Exception:
        print("Error")


def data_to_list(data):
    list = []
    for row in data:
        row_to_list = [elem for elem in row]
        list.append(row_to_list)
    return list


def get_users_stocks_by_user_id(user_id):
    """
    get_users_stocks_by_user_id is a function that gets a user id and returns all of the users stocks
    :param user_id: the user id to search for
    :return: list of Stocks
    """
    # get data from db
    stock_data = execute_select_query(sql="SELECT * FROM dbo.Stocks WHERE user_id=" + str(user_id))
    # convert data to list
    list_of_stocks = data_to_list(stock_data)
    # move data to list of all stocks
    return_user_stocks_list = []
    temp_stock = 0
    for stock in list_of_stocks:
        ticker = stock[1]
        amount_of_stocks = stock[2]
        cost = stock[4]
        purchase_date = str(stock[5])
        temp_stock = Stock.Stock(ticker=ticker, amount_of_stocks=amount_of_stocks, cost=cost,
                                 purchase_date=purchase_date)
        return_user_stocks_list.append(temp_stock)
    return return_user_stocks_list


def get_users_stock_by_ticker(user_id, ticker):
    try:
        sql = "SELECT * FROM dbo.Stocks WHERE ticker='" + ticker + "' AND user_id=" + str(user_id)
        data = execute_select_query(sql)
        data = data_to_list(data)
        return Stock.Stock(ticker=data[0][1], amount_of_stocks=data[0][2], cost=data[0][4], purchase_date=data[0][5])
    except Exception as e:
        print("Error... " + str(e))


def get_users_stocks_by_email(email):
    """
     get_users_stocks_by_user_id is a function that gets an email and returns all of the users stocks
    :param email:
    :return:
    """
    return get_users_stocks_by_user_id(user_id=get_user_id_by_email(email))


def print_all_users():
    """
    print_all_users is a function that prints all users from the Users table
    :return: None
    """
    data = execute_select_query("SELECT * FROM dbo.Users")
    print("[id   FirstName   LastName   Email                            Password]")
    for row in data:
        print(row)


def print_all_stocks():
    """
    print_all_users is a function that prints all stocks from the Stocks table
    :return: None
    """
    data = execute_select_query("SELECT * FROM dbo.Stocks")
    print("[id   ticker   amount_of_stocks   user_id cost]")
    for row in data:
        print(row)


def remove_stock_by_user_id(ticker, user_id):
    """
    remove_stock_by_user_id is a function that removes a stocks by the user's id
    :param ticker: the stocks ticker
    :param user_id: the user's id
    :return: None
    """
    execute_query(sql="DELETE FROM dbo.Stocks WHERE ticker='" + ticker + "' AND user_id=" + str(user_id))
    print("Stock removed from db")


def remove_user_by_email(email):
    """
      remove_stock_by_email is a function that removes a user and its stocks from db by the user's id
      :param user_id: the user's email
      :return: None
      """
    remove_user_by_user_id(get_user_id_by_email(email=str(email)))


def update_stock(ticker, user_id, amount_of_stocks=-1, cost=-1, purchese_date=-1):
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
        if amount_of_stocks == -1 or cost == -1 or purchese_date == -1:
            stock = get_users_stock_by_ticker(ticker=ticker, user_id=user_id)
            if amount_of_stocks == -1:
                amount_of_stocks = stock.get_amount_of_stocks()
            elif cost == -1:
                cost = stock.get_cost()
            else:
                purchese_date = stock._purchase_date

        execute_query(
            "UPDATE dbo.Stocks SET amount_of_stocks =" + str(amount_of_stocks) + " , cost = " + str(
                cost) + ",purchese_date='" + str(purchese_date) + "'  WHERE user_id =" + str(
                user_id) + "  AND ticker = '" + ticker + "'")
        print("Stock has been updated")
    except Exception as e:
        print("Error  " + str(e))
        cost = stock.get_cost()


def check_user_details(email, password):
    if is_exist(sql="SELECT * FROM dbo.Users WHERE Email='" + str(email) + "' AND Password='" + str(password) + "'"):
        print("User in db")
        return True
    else:
        print("Incorrect details")
        return False


def stock_exists(user_id, ticker):
    return is_exist("SELECT * FROM dbo.Stocks WHERE user_id=" + str(user_id) + "AND ticker='" + ticker + "'")


def main():
   pass


if __name__ == '__main__':
    main()
