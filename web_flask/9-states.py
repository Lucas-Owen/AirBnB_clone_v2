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
    """Tears down the context"""
    storage.close()


@app.route("/states")
def get_all_states():
    """Render all states"""
    return render_template("9-states.html", states=storage.all(State).values())


@app.route("/states/<id>")
def get_state_by_id(id):
    """Render a city with its state"""
    res = list(filter(lambda x: x.id == id, storage.all(State).values()))
    state = res[0] if res else None
    return render_template("9-states.html",
                           state=state)


if __name__ == "__main__":
    app.run()
