#!/usr/bin/python3
"""This module defines a simple flask application"""


from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_HBNB():
    """This function returns 'Hello HBNB!'"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run()
