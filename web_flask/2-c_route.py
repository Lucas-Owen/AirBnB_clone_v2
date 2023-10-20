#!/usr/bin/python3
"""This module defines a simple flask application"""


from flask import Flask
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
def path(text):
    """This function returns 'HBNB'"""
    return f"C {escape(text.replace('_', ' '))}"


if __name__ == "__main__":
    app.run()
