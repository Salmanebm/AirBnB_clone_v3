#!/usr/bin/python3
""" Amenity view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_amenities():
    """ Lists all City objects """
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_id(amenity_id):
    """ Returns the City object with the given id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_id(amenity_id):
    """ Deletes an object via its ID """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates a new object """
    header_data = request.get_json()
    if header_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in header_data.keys():
        abort(400, 'Missing name')
    new_amenity = Amenity(**header_data)
    storage.new(new_amenity)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ Update an existing amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    header_data = request.get_json()
    if header_data is None:
        abort(400, 'Not a JSON')

    for k, v in header_data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)

    storage.save()
    return jsonify(amenity.to_dict()), 200
