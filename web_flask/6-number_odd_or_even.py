#!/usr/bin/python3
"""This module defines a simple flask application"""


from flask import Flask
from flask import render_template
from markupsafe import escape

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def hello_HBNB():
    """This function returns 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route("/hbnb")
def HBNB():
    """This function returns 'HBNB'"""
    return "HBNB"


@app.route("/c/<text>")
def variable_route(text):
    """This function returns some text"""
    return f"C {escape(text.replace('_', ' '))}"


@app.route("/python")
@app.route("/python/<text>")
def default_variable_route(text="is cool"):
    """This function returns some text"""
    return f"Python {escape(text.replace('_', ' '))}"


@app.route("/number/<int:n>")
def number(n):
    """This function returns some text"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>")
def number_template(n):
    """This function returns some text"""
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>")
def number_odd_or_even_template(n):
    """This function returns some text"""
    return render_template("6-number_odd_or_even.html", n=n)


if __name__ == "__main__":
    app.run()
