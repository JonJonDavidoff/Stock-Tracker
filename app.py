# -*- coding: UTF-8 -*-
"""
hello_flask: First Python-Flask webapp
"""
from flask import Flask, render_template  # Need render_template() to render HTML pages
app = Flask(__name__)    # Construct an instance of Flask class for our webapp

@app.route('/')   # URL '/' to be handled by main() route handler
def main():
    """Say hello"""
    return render_template('index.html')

if __name__ == '__main__':  # Script executed directly?
    app.run()

