#!/usr/bin/python3
""" Review view """

from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def list_reviews(place_id):
    """ lists all reviews objects that are linked to a specific place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])

