#!/usr/bin/python3
""" view for user object """
from . import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_user():
    """ retrieve all users """
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_id(user_id):
    """ retrieve a user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ delete a user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """
    Creates a City object
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    instance = User(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a City object."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()

    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
