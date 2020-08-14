import DbApi


# TODO pytest
def main():
    # DbApi.execute_query(sql="INSERT INTO dbo.Users VALUES('Jon Jon', 'Davidoff','jonjondavidofff@gmail.com')")
    # DbApi.execute_query(sql="UPDATE dbo.Users SET Email='edfd' WHERE id=2")
    # data = DbApi.execute_select_query(sql="SELECT * FROM dbo.Users")
    # for row in data:
    #     print(row)
    # # DbApi.execute_query(sql="DELETE FROM dbo.Users WHERE id = 2")
    # data = DbApi.execute_select_query(sql="SELECT * FROM dbo.Users")
    # print("--------------------------------------------------------")
    # for row in data:
    #     print(row)
    # DbApi.add_user('Jon Jon', 'Davidoff', 'jonjondavidofff@gmail.com', 'Jonjon1212')  # user that already exists
    # print("---------------------------------")
    # print("get user by email: ")
    # user = DbApi.get_user_by_email('jonjondavidofff@gmail.com')
    # print(user)
    # print("get user by id: ")
    # user = DbApi.get_user_by_id(id=1)
    # print(user)
    # # insert of a new stock
    # DbApi.add_stock(ticker='AMZN', user_id=1, cost_of_stock=1960, amount_of_stocks=1)
    # # get users stocks by user id
    # print("get users stocks by user id")
    # list_of_stocks = DbApi.get_users_stocks_by_user_id(1)
    # for stock in list_of_stocks:
    #     print(stock)
    # print("get users Stocks by email")
    # DbApi.add_stock(ticker='CVS', user_id=1)
    # list_of_stocks = DbApi.get_users_stocks_by_email(email="jonjondavidofff@gmail.com")
    # for stock in list_of_stocks:
    #     print(stock)
    # DbApi.print_all_users()
    # DbApi.print_all_stocks()
    # print("Remove stock by user id that does not exist")
    # DbApi.remove_stock_by_user_id(ticker='CVS', user_id=2)
    # DbApi.print_all_stocks()
    # print("Remove stock by user id that does  exist")
    # DbApi.remove_stock_by_user_id(ticker='CVS', user_id=1)
    # DbApi.print_all_stocks()
    # print("Remove user")
    # DbApi.add_user("asfd", "fdsfd", "fddfa@gmail.com", "Ddfjgj1213")
    # DbApi.add_stock(user_id=DbApi.get_user_id_by_email(email="fddfa@gmail.com"),ticker='AAPL')
    # DbApi.print_all_stocks()
    # DbApi.print_all_users()
    # DbApi.remove_user(user_id=DbApi.get_user_id_by_email(email="fddfa@gmail.com"))
    # DbApi.print_all_stocks()
    DbApi.print_all_users()
    # DbApi.update_stock(ticker='AMZN', user_id=1, amount_of_stocks=1, cost=1960)
    # DbApi.print_all_stocks()
    # DbApi.update_stock(ticker='AMZN', user_id=1, amount_of_stocks=1, cost=1960)
    # DbApi.print_all_stocks()
    # DbApi.get_users_stocks_by_user_id(user_id=1)

if __name__ == '__main__':
    main()
