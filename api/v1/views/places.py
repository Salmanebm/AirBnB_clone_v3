#!/usr/bin/python3
""" Place view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def list_places(city_id):
    """ Lists all City objects """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place_id(place_id):
    """ Returns the City object with the given id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_Place_id(place_id):
    """ Deletes an object via its ID """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_Place(city_id):
    """ Creates a new object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    header_data = request.get_json()
    if header_data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in header_data.keys():
        abort(400, 'Missing user_id')
    user = storage.get(User, header_data.user_id)
    if not user:
        abort(400)
    if 'name' not in header_data.keys():
        abort(400, 'Missing name')
    new_Place = Place(**header_data, city_id=city_id)
    storage.new(new_Place)
    new_Place.save()
    return jsonify(new_Place.to_dict()), 201


@app_views.route('places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_Place(place_id):
    """ Update an existing Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    header_data = request.get_json()
    if header_data is None:
        abort(400, 'Not a JSON')

    for k, v in header_data.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(Place, k, v)

    storage.save()
    return jsonify(Place.to_dict()), 200
