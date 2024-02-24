#!/usr/bin/python3
"""First api"""

from flask import Flask
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)