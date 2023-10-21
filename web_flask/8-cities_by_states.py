#!/usr/bin/python3
"""This module runs a simple flask app"""


from flask import Flask
from flask import render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(exception):
    """Closes the storage session"""
    storage.close()


@app.route("/cities_by_states")
def get_cities_by_state():
    """Renders a template of cities by states"""
    return render_template("8-cities_by_states.html",
                           states=storage.all(State).values())


if __name__ == "__main__":
    app.run()
