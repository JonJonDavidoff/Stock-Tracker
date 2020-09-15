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

app = Flask(__name__, static_url_path='/static')  # Construct an instance of Flask class for our webapp
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)


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
    return render_template('index.html')


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
                return redirect(url_for('login'))
            except Exception as e:
                DbApi.remove_user_by_email(str(data['Email']))
                print(str(e))
        else:
            try:
                return redirect(url_for('user_exists'))
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


@app.route('/search_stock_form', methods=['POST'])
def search_stock_form():
    try:
        if request.method == "POST":
            return Stock.Stock(ticker=request.form['stock-input'].upper()).__str__()
    except Exception as e:
        print(str(e))
        return "Please enter only a ticker"


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('conn event')
def handle_an_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived())


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
            # Getting Stock Data
            stock = Stock.Stock(ticker=ticker, amount_of_stocks=shares, cost=cost_per_share,
                                purchase_date=purchase_date)
            socketio.emit('response_adding_table_row', stock.convert_main_stock_data_to_json())
        except Exception as e:
            # TODO Add Exception to Ui
            print(str(e))


if __name__ == '__main__':  # Script executed directly?
    socketio.run(app, debug=True, host="")
