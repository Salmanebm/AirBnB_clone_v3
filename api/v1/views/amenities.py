#!/usr/bin/python3
""" Amenity view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_amenities():
    """ Lists all Amenities objects """
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_id(amenity_id):
    """ Returns the amenity object with the given id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_id(amenity_id):
    """ Deletes an amenity object via its ID """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates a new amenity object """
    if not request.is_json:
        abort(400, 'Not a JSON')

    if 'name' not in request.get_json().keys():
        abort(400, 'Missing name')

    new_amenity = Amenity(**request.get_json())
    storage.new(new_amenity)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an existing amenity object """
    if not request.is_json:
        abort(400, 'Not a JSON')

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)

    storage.save()
    return jsonify(amenity.to_dict()), 200
