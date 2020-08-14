# -*- coding: UTF-8 -*-
"""
hello_flask: First Python-Flask webapp
"""
from flask import Flask, render_template, request, url_for  # Need render_template() to render HTML pages

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


@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']
    print(projectpath)
    return render_template('home.html')
    # your code
    # return a response


@app.route('/addRegion', methods=['POST'])
def addRegion():
    projectpath = request.form['projectFilepath']
    print(projectpath)


if __name__ == '__main__':  # Script executed directly?
    app.run(debug=True, host="")
