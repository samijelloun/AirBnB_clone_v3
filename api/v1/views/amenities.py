#!/usr/bin/python3
"""  """
from flask import make_response, jsonify, request, abort
from . import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.user import User


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    all_amenities = storage.all(Amenity)
    amenity_list = []
    for amenity in all_amenities.values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenities_id(amenity_id=None):
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenities(amenity_id=None):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    json_in = request.get_json(silent=True)
    if not json_in:
        abort(400, 'Not a JSON')
    if 'name' not in json_in:
        abort(400, 'Missing name')
    amenity = Amenity(**json_in)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity_json_in = request.get_json(silent=True)
    if not amenity_json_in:
        abort(400, 'Not a JSON')
    for key, value in amenity_json_in.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
