#!/usr/bin/python3
"""
View for Place objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Retrieves a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
    Creates a Place
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')

    user_id = request.get_json().get('user_id')
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    data = request.get_json()
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    Updates a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
    Retrieves all Place objects based on the JSON body request
    """
    if request.get_json() is not None:
        params = request.get_json()
        states = params.get('states', [])
        cities = params.get('cities', [])
        amenities = params.get('amenities', [])
        amenity_objects = []
        for amenity_id in amenities:
            amenity = storage.get('Amenity', amenity_id)
            if amenity:
                amenity_objects.append(amenity)
        if states == cities == []:
            places = storage.all('Place').values()
        else:
            places = []
            for state_id in states:
                state = storage.get('State', state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get('City', city_id)
                for place in city.places:
                    places.append(place)
        confirmed_places = []
        for place in places:
            place_amenities = place.amenities
            confirmed_places.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    confirmed_places.pop()
                    break
        return jsonify(confirmed_places)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
