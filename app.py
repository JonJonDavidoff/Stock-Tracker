# -*- coding: UTF-8 -*-
"""
hello_flask: First Python-Flask webapp
"""

from flask import Flask, render_template, request, url_for, redirect, \
    session  # Need render_template() to render HTML pages
import bridging_users_db
import Stock
import DbApi
from flask_socketio import SocketIO
import json
from threading import Thread, Lock
from time import sleep
import stock_api_exceptions
import Logger
import sys
import StockWithHistory


app = Flask(__name__, static_url_path='/static')  # Construct an instance of Flask class for our webapp
app.config['SECRET_KEY'] = 'SECRET'
socketio = SocketIO(app)
ticker = None
stock_dashboard_thread = None
is_stock_dashboard_thread_live: bool = False
usernameExsits = False


@app.route('/stock_page')
def stock_page():
    return render_template('stock.html')


@app.route('/')  # URL '/' to be handled by main() route handler
def main():
    """Say hello"""
    return render_template('home.html')


@app.route('/login.html')
def login():
    return render_template('login.html')


@app.route('/signup.html')
def signup():
    global usernameExsits
    if usernameExsits:
        socketio.emit('user_exists', json.dumps({
            'hellp' : 'h',
        }))
        usernameExsits = False
        print('done')
    return render_template('signup.html')


@app.route('/user_exists.html')
def user_exists():
    return render_template('user_exists.html')


@app.route('/index.html')
def stock_dashboard():
    print(session['Email'])
    if session['Email']:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/signup_form', methods=['POST'])
def signup_form():
    # Stop the form from transferring data before submit
    if request.method == "POST":
        # getting data from form
        data = request.form
        # casting to dict
        data = dict(data)
        if bridging_users_db.excecute_signup(data):
            try:
                session['Email'] = data['Email']
                session['isLoggedIn'] = True
                return redirect(url_for('stock_dashboard'))
            except Exception as e:
                DbApi.remove_user_by_email(str(data['Email']))
                print(str(e))
        else:
            try:
                global usernameExsits
                usernameExsits = True
                return redirect(url_for('signup'))
            except Exception as e:
                print(str(e))


@app.route('/login_form', methods=['POST'])
def login_form():
    # When loading form already transfers details
    if request.method == "POST":
        form_data_dict = dict(request.form)
        print(str(form_data_dict))
        if bridging_users_db.excecute_login(form_data_dict):
            session['Email'] = form_data_dict['Email']
            # TODO Transfer data
            return redirect(url_for('stock_dashboard'))
        else:
            return redirect(url_for('signup'))


@app.route('/logout')
def logout():
    session.pop('SECRET', None)
    session['Email'] = None
    session['ticker'] = None
    return redirect(url_for('main'))


@app.route("/stocks", methods=['GET', 'POST'])
def on_stocks():
    global stock_dashboard_thread
    global is_stock_dashboard_thread_live
    url_dict = request.args.to_dict()
    session['Email'] = session['Email']
    session['ticker'] = url_dict[' ticker']
    try:
        stock_dashboard_thread.join()
        stock_dashboard_thread = None
        is_stock_dashboard_thread_live = False
    except Exception:
        pass
    return redirect(url_for('stock_page'))


def parse_args(arg_dict):
    try:
        print("parse " + str(arg_dict['ticker']))
        session['ticker'] = arg_dict['ticker']
    except Exception as e:
        print(str(e))


@socketio.on('dashboard_load_request')
def handle_an_event(json_data, methods=['GET', 'POST']):
    stock_table = bridging_users_db.get_stocks_data_by_email(session['Email'])
    stock_diversity_list = Stock.get_sector_diversity(stock_table)
    list_of_stocks_json = []
    for stock in stock_table:
        list_of_stocks_json.append(stock.convert_main_stock_data_to_json())
    print(list_of_stocks_json)
    socketio.emit('dashboard_load_response',
                  json.dumps((json.dumps(list_of_stocks_json), json.dumps(stock_diversity_list))))
    # Update live data
    global stock_dashboard_thread
    global is_stock_dashboard_thread_live
    stock_dashboard_thread = None
    stock_dashboard_thread = Thread(target=update_data, args=(stock_table,))
    is_stock_dashboard_thread_live = True
    sleep(20)
    stock_dashboard_thread.start()
    stock_dashboard_thread.join()
    is_stock_dashboard_thread_live = False
    stock_dashboard_thread = None


@socketio.on('add_transaction')
def add_transaction(json, methods=['GET', 'POST']):
    if json:
        print(str(json))
        # Assigning data to variables
        ticker = json['ticker']
        email = session['Email']
        shares = json['shares']
        cost_per_share = json['costPerShare']
        purchase_date = json['purchaseDate']
        try:
            # Adding Stock to DB
            # TODO Change to Update
            DbApi.remove_stock_by_user_id(user_id=DbApi.get_user_id_by_email(email), ticker=ticker)
            DbApi.add_stock_by_email(email=email, ticker=ticker, purchese_date=purchase_date,
                                     cost_of_stock=cost_per_share,
                                     amount_of_stocks=shares)
            socketio.emit('response_adding_table_row')
        except Exception as e:
            # TODO Add Exception to Ui
            print(str(e))


@socketio.on('onload')
def stock_page_on_load():
    try:
        try:
            global is_stock_dashboard_thread_live
            global stock_dashboard_thread
            stock_dashboard_thread.join()
            is_stock_dashboard_thread_live = False
            stock_dashboard_thread = None
        except Exception:
            pass
        is_user_holding_stock = DbApi.stock_exists(user_id=DbApi.get_user_id_by_email(session['Email']),
                                                   ticker=session['ticker'])
        stock = StockWithHistory.StockWithHistory(ticker=session['ticker'])
        stock_json = stock.convert_main_stock_data_to_json()
        stock_json['is_user_holding_stock'] = is_user_holding_stock
        stock_json['graph_1d'] = stock._one_day_historical_data
        stock_json['graph_5d'] = stock._five_day_historical_data
        stock_json['graph_1m'] = stock.one_month_data
        stock_json['graph_3m'] = stock._three_month_historical_data
        stock_json['graph_6m'] = stock._six_month_historical_data
        stock_json['graph_ytd'] = stock._ytd_historical_data
        stock_json['graph_1y'] = stock._1y_historical_data
        stock_json['graph_5y'] = stock._5y_historical_data
        stock_json['graph_max'] = stock._max_historical_data
        socketio.emit('page_load_response', json.dumps(stock_json))
    except stock_api_exceptions.UnknownSymbolException as e:
        print(sys.exc_info())
        Logger.Log.get_log().log(file_name='Stock.py', exception=str(e), function_name='get_company_name')
        socketio.emit("ticker_not_found", json.dumps({'ticker': session['ticker']}))
    except Exception as e:
        print(e)


@socketio.on('addStock')
def add_stock(json, methods=['GET', 'POST']):
    DbApi.add_stock_by_email(session['Email'], str(session['ticker']), -1, 0, 'False')


@socketio.on('removeStock')
def remove_stock(json, methods=['GET', 'POST']):
    DbApi.remove_stock_by_user_id(ticker=str(session['ticker']), user_id=DbApi.get_user_id_by_email(session['Email']))


lock = Lock()


def update_data(list_of_stocks):
    json_list_of_stocks = []
    sleep(0)
    global is_stock_dashboard_thread_live
    global stock_dashboard_thread
    while True:
        if not is_stock_dashboard_thread_live:
            break
        json_list_of_stocks.clear()
        lock.acquire()
        for stock in list_of_stocks:
            stock.update_stock()
            json_list_of_stocks.append(stock.convert_main_stock_data_to_json())
        socketio.emit('update_data', json.dumps(json_list_of_stocks))
        lock.release()
        print("Update")
        sleep(200)


if __name__ == '__main__':  # Script executed directly?
    socketio.run(app, debug=True, host="")
#     dfadf
