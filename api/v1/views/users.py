#!/usr/bin/python3
"""
View for User objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    """
    Retrieves the list of all User objects
    """
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieves a User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'])
def create_user():
    """
    Creates a User
    """
    if not request.get_json():
        abort(400, 'Not a JSON')

    if 'email' not in request.get_json():
        abort(400, 'Missing email')

    if 'password' not in request.get_json():
        abort(400, 'Missing password')

    data = request.get_json()
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates a User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
