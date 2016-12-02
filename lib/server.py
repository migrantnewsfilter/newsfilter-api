from __future__ import print_function # In python 2.7
from flask import Flask, request
from flask_socketio import SocketIO
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.json_util import dumps
from flask_cors import CORS, cross_origin
from BeautifulSoup import BeautifulSoup
from toolz import assoc_in
import os
import sys


# Make app
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# Connect to Mongo --> TODO: close connection on shutdown hook!
client = MongoClient(
    host = os.environ.get('MONGO_HOST') or None
)


@socketio.on('label')
def handle_label(data):
    collection = client['newsfilter'].news
    collection.update_one({ '_id': data['_id']}, {'$set': {'label': data['label']}})


@app.route('/terms')
def get_sources():
    collection = client['newsfilter'].terms
    cursor = collection.find()
    return dumps(cursor)


@app.route('/articles/')
def get_articles():
    collection = client['newsfilter'].news
    request.args.get('relevance')
    start = int(request.args.get('start')) or 0

    cursor = collection.aggregate([
        { '$match': { 'label': None }},
        { '$sort': { 'prediction': 1, 'published': 1 }},
        { '$group': { '_id': '$cluster', 'item': { '$first': '$$ROOT' }}}
    ])
    # get similar
    l = list(cursor)[start: start+20]
    return dumps(map(lambda x: x['item'] , l))

def run():
    socketio.run(app, '0.0.0.0')
