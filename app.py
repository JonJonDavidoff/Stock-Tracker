# -*- coding: UTF-8 -*-
"""
hello_flask: First Python-Flask webapp
"""
from flask import Flask, render_template, request, url_for  # Need render_template() to render HTML pages
import bridging_users_db

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


@app.route('/signup_form', methods=['POST'])
def signup_form():
    # When loading form already transfers details
    # getting data from form
    data = request.form
    # casting to dict
    data = dict(data)

    if bridging_users_db.excecute_signup(data):
        try:
            return render_template('login.html')
        except Exception as e:
            print(str(e))
    else:
        try:
            return render_template('user_exists.html')
        except Exception as e:
            print(str(e))


@app.route('/login_form', methods=['POST'])
def login_form():
    # When loading form already transfers details
    if request.form['Login'] != None:
        if bridging_users_db.excecute_login(dict(request.form)):
            return render_template('stock_dashboard.html')
        else:
            return render_template('Signup.html')



if __name__ == '__main__':  # Script executed directly?
    app.run(debug=True, host="")
