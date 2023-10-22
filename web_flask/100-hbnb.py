#!/usr/bin/python3
"""This module runs a simple flask app"""


from flask import Flask, render_template
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(exception):
    """Tears down context"""
    storage.close()


@app.route("/hbnb")
def get_hbnb():
    """Render 100-hbnb.html"""
    return render_template(
        "100-hbnb.html",
        states=storage.all(State).values(),
        cities=storage.all(City).values(),
        amenities=storage.all(Amenity).values(),
        places=storage.all(Place).values()
    )


if __name__ == "__main__":
    app.run()
