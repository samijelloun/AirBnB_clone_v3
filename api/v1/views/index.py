#!/usr/bin/python3
"""  """
from flask import jsonify
from . import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['Get'])
def get_status():
    """Endpoint to check the status of the API"""
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', methods=['GET'])
def count():
    dic_count = {}
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    for key, obj in classes.items():
        dic_count[key] = storage.count(obj)
    return jsonify(dic_count)
