#!/usr/bin/python3
"""
View for City objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'])
def get_city(city_id):
    """
    Retrieves a City object
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes a City object
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    city.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<string:state_id>/cities', methods=['POST'])
def create_city(state_id):
    """
    Creates a City
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    data = request.get_json()
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'])
def update_city(city_id):
    """
    Updates a City object
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
