#!/usr/bin/python3
""" New view for User object that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    """ Lists all User objects """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


# @app_views.route('/users/<string:user_id>', methods=['GET'],
#                  strict_slashes=False)
# def user_id(user_id):
#     """ Returns the User object with the given id """
#     user = storage.get(User, user_id)
#     if user is None:
#         abort(404)
#     return jsonify(user.to_dict())


# @app_views.route('/users/<user_id>', methods=['DELETE'],
#                  strict_slashes=False)
# def delete_user_id(user_id):
#     """ Deletes an object via its ID """
#     user = storage.get(User, user_id)
#     if user is None:
#         abort(404)
#     user.delete()
#     storage.save()
#     return jsonify({}), 200


# @app_views.route('/users', methods=['POST'], strict_slashes=False)
# def create_user():
#     """ Creates a new object """
#     header_data = request.get_json()
#     if header_data is None:
#         abort(400, 'Not a JSON')
#     if 'name' not in header_data.keys():
#         abort(400, 'Missing name')
#     new_user = User(**header_data)
#     storage.new(new_user)
#     new_user.save()
#     return jsonify(new_user.to_dict()), 201


# @app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
# def update_user(user_id):
#     """ Update an existing User object """
#     user = storage.get(User, user_id)
#     if user is None:
#         abort(404)

#     header_data = request.get_json()
#     if header_data is None:
#         abort(400, 'Not a JSON')

#     for k, v in header_data.items():
#         if k not in ['id', 'email', 'created_at', 'updated_at']:
#             setattr(user, k, v)

#     storage.save()
#     return jsonify(user.to_dict()), 200
