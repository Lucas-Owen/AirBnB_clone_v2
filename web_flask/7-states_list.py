#!/usr/bin/python3
"""This module starts a flask application"""


from flask import Flask
from flask import render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(exception):
    """Closes the session"""
    storage.close()


@app.route("/states_list")
def get_states():
    """Displays an unordered list of all states"""
    states = storage.all(State).values()
    return render_template("7-states_list.html", states=states)


if __name__ == "__main__":
    app.run()
