import DbApi, app
from requests import request


# TODO Testing excecute_signup
def excecute_signup(form_data):
    try:
        print(form_data)
        # creating api instance
        # using add user function to try to add the user to db
        if DbApi.add_user(first_name=form_data['FirstName'], last_name=form_data['LastName'], email=form_data['Email'],
                          password=form_data['Password']):
            return True
        else:
            return False
    except Exception as e:
        pass


# TODO Testing execute_login
def excecute_login(form_data):
    if DbApi.check_user_details(email=form_data['Email'], password=form_data['Password']):
        return True
    else:
        return False


def get_stocks_data_by_email(email):
    return DbApi.get_users_stocks_by_email(email)


def get_onload_stock_data(list_of_stocks):
    pass
