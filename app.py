# -*- coding: UTF-8 -*-
"""
hello_flask: First Python-Flask webapp
"""
from flask import Flask, render_template, request, url_for, redirect  # Need render_template() to render HTML pages
import bridging_users_db
import Stock
import DbApi

app = Flask(__name__, static_url_path='/static')  # Construct an instance of Flask class for our webapp


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


@app.route('/stock_dashboard.html')
def stock_dashboard():
    return render_template('stock_dashboard.html')


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
        if bridging_users_db.excecute_login(form_data_dict):
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


if __name__ == '__main__':  # Script executed directly?
    app.run(debug=True, host="")
