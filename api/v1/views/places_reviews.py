#!/usr/bin/python3
""" Review view """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def list_reviews(place_id):
    """ lists all reviews objects that are linked to a specific place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review_id(review_id):
    """ Retrieves an object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes an existing object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ Creates a new post object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    
    header_data = request.get_json()
    if not header_data:
        abort(400, 'Not a JSON')
    
    if 'user_id' not in header_data.keys():
        abort(400, 'Missing user_id')
    
    user = storage.get(User, header_data.get('user_id'))
