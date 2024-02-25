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
    """ Lists all State objects """
    return jsonify([city.to_dict() for city in storage.all(City)
                    .values() if city.state_id == state_id])


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def city_id(city_id):
    """ Returns the State object with the given id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


# @app_views.route('states/<state_id>', methods=['DELETE'],
#                  strict_slashes=False)
# def delete_state_id(state_id):
#     """ Deletes an object via its ID """
#     state = storage.get(City, state_id)
#     if state is None:
#         abort(404)
#     state.delete()
#     storage.save()
#     return jsonify({}), 200


# @app_views.route('/states', methods=['POST'], strict_slashes=False)
# def create_state():
#     """ Creates a new object """
#     header_data = request.get_json()
#     if header_data is None:
#         abort(400, 'Not a JSON')
#     if 'name' not in header_data.keys():
#         abort(400, 'Missing name')
#     new_state = City(**header_data)
#     storage.new(new_state)
#     new_state.save()
#     return jsonify(new_state.to_dict()), 201


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
