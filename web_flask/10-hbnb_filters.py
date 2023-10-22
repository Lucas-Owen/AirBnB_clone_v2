#!/usr/bin/python3
"""This module runs a simple flask app"""


from flask import Flask
from flask import render_template
from models import storage
from models.amenity import Amenity
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(exception):
    """Tear down app context"""
    storage.close()


@app.route("/hbnb_filters")
def get_hbnb_filters():
    """Render hbnb_filters"""
    return render_template("10-hbnb_filters.html",
                           states=storage.all(State).values(),
                           amenities=storage.all(Amenity).values())


if __name__ == "__main__":
    app.run()
