#!/usr/bin/python3
"""  """
from flask import make_response, jsonify, request, abort
from . import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    all_states = storage.all(State)
    state_list = []
    for state in all_states.values():
        state_list.append(state.to_dict())
    return jsonify(state_list), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_id(state_id=None):
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_states(state_id=None):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        storage.delete(city)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    json_in = request.get_json(silent=True)
    if not json_in:
        abort(400, 'Not a JSON')
    if 'name' not in json_in:
        abort(400, 'Missing name')
    state = State(**json_in)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state_json_in = request.get_json(silent=True)
    if not state_json_in:
        abort(400, 'Not a JSON')
    for key, value in state_json_in.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())
