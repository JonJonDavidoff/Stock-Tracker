import DbApi


# TODO pytest
def main():
    dbApi = DbApi.DbApi()
    dbApi.execute_query(sql="INSERT INTO dbo.Users VALUES('Jon Jon', 'Davidoff','jonjondavidofff@gmail.com')")
    dbApi.execute_query(sql="UPDATE dbo.Users SET Email='edfd' WHERE id=2")
    data = dbApi.execute_select_query(sql="SELECT * FROM dbo.Users")
    for row in data:
        print(row)
    # dbApi.execute_query(sql="DELETE FROM dbo.Users WHERE id = 2")
    data = dbApi.execute_select_query(sql="SELECT * FROM dbo.Users")
    print("--------------------------------------------------------")
    for row in data:
        print(row)
    dbApi.add_user('Jon Jon', 'Davidoff', 'jonjondavidofff@gmail.com', 'Jonjon1212')  # user that already exists
    print("---------------------------------")
    print("get user by email: ")
    user = dbApi.get_user_by_email('jonjondavidofff@gmail.com')
    print(user)
    print("get user by id: ")
    user = dbApi.get_user_by_id(id=1)
    print(user)
    # insert of a new stock
    dbApi.add_stock(ticker='AMZN', user_id=1, cost_of_stock=1960, amount_of_stocks=1)
    # get users stocks by user id
    print("get users stocks by user id")
    list_of_stocks = dbApi.get_users_stocks_by_user_id(1)
    for stock in list_of_stocks:
        print(stock)
    print("get users Stocks by email")
    dbApi.add_stock(ticker='CVS', user_id=1)
    list_of_stocks = dbApi.get_users_stocks_by_email(email="jonjondavidofff@gmail.com")
    for stock in list_of_stocks:
        print(stock)
    dbApi.print_all_users()
    dbApi.print_all_stocks()
    print("Remove stock by user id that does not exist")
    dbApi.remove_stock_by_user_id(ticker='CVS', user_id=2)
    dbApi.print_all_stocks()
    print("Remove stock by user id that does  exist")
    dbApi.remove_stock_by_user_id(ticker='CVS', user_id=1)
    dbApi.print_all_stocks()
    print("Remove user")
    dbApi.add_user("asfd", "fdsfd", "fddfa@gmail.com", "Ddfjgj1213")
    dbApi.add_stock(user_id=dbApi.get_user_id_by_email(email="fddfa@gmail.com"),ticker='AAPL')
    dbApi.print_all_stocks()
    dbApi.print_all_users()
    dbApi.remove_user(user_id=dbApi.get_user_id_by_email(email="fddfa@gmail.com"))
    dbApi.print_all_stocks()
    dbApi.print_all_users()
    dbApi.update_stock(ticker='AMZN', user_id=1, amount_of_stocks=1, cost=1960)
    dbApi.print_all_stocks()
    dbApi.update_stock(ticker='AMZN', user_id=1, amount_of_stocks=1, cost=1960)
    dbApi.print_all_stocks()
    dbApi.get_users_stocks_by_user_id(user_id=1)

if __name__ == '__main__':
    main()
