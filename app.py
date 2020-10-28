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

app = Flask(__name__, static_url_path='/static')  # Construct an instance of Flask class for our webapp
app.config['SECRET_KEY'] = 'SECRET'
socketio = SocketIO(app)
ticker = None


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
            stock_table = bridging_users_db.get_stocks_data_by_email(email=form_data_dict['Email'])
            session['Email'] = form_data_dict['Email']
            for stock in stock_table:
                print(stock.convert_main_stock_data_to_json())
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
    print(str(request.args.to_dict()))
    url_dict = request.args.to_dict()
    session['Email'] = session['Email']
    session['ticker'] = url_dict[' ticker']
    return redirect(url_for('stock_page'))


def parse_args(arg_dict):
    try:
        print("parse " + str(arg_dict['ticker']))
        session['ticker'] = arg_dict['ticker']
    except Exception as e:
        print(str(e))


@socketio.on('dashboard_load_request')
def handle_an_event(json_data, methods=['GET', 'POST']):
    print('recived event')
    stock_table = bridging_users_db.get_stocks_data_by_email(session['Email'])
    stock_diversity_list = Stock.get_sector_diversity(stock_table)
    list_of_stocks_json = []
    for stock in stock_table:
        list_of_stocks_json.append(stock.convert_main_stock_data_to_json())
    print(list_of_stocks_json)
    socketio.emit('dashboard_load_response', json.dumps((json.dumps(list_of_stocks_json), json.dumps(stock_diversity_list))))


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
    is_user_holding_stock = DbApi.stock_exists(user_id=DbApi.get_user_id_by_email(session['Email']),
                                               ticker=session['ticker'])
    stock_json = Stock.Stock(ticker=session['ticker']).convert_main_stock_data_to_json()
    stock_json['is_user_holding_stock'] = is_user_holding_stock
    socketio.emit('page_load_response', json.dumps(stock_json))


@socketio.on('addStock')
def add_stock(json, methods=['GET', 'POST']):
    DbApi.add_stock_by_email(session['Email'], str(session['ticker']), -1, 0, 'False')


@socketio.on('removeStock')
def remove_stock(json, methods=['GET', 'POST']):
    DbApi.remove_stock_by_user_id(ticker=str(session['ticker']), user_id=DbApi.get_user_id_by_email(session['Email']))


if __name__ == '__main__':  # Script executed directly?
    socketio.run(app, debug=True, host="")
