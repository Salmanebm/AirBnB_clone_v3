#!/usr/bin/python3
""" City view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def list_cities(state_id):
    """ Lists all City objects """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def city_id(city_id):
    """ Returns the City object with the given id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_id(city_id):
    """ Deletes an object via its ID """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a new object """
    if not storage.get(State, state_id):
        abort(404)

    header_data = request.get_json()
    if header_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in header_data.keys():
        abort(400, 'Missing name')
    new_city = City(**header_data, state_id=state_id)
    storage.new(new_city)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


# @app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
# def update_state(state_id):
#     """ Update an existing state object """
#     state = storage.get(City, state_id)
#     if state is None:
#         abort(404)

#     header_data = request.get_json()
#     if header_data is None:
#         abort(400, 'Not a JSON')

#     for k, v in header_data.items():
#         if k not in ['id', 'created_at', 'updated_at']:
#             setattr(state, k, v)

#     storage.save()
#     return jsonify(state.to_dict()), 200
