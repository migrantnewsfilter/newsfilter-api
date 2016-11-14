from __future__ import print_function # In python 2.7
from flask import Flask
from flask_socketio import SocketIO
from pymongo import MongoClient, ASCENDING
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
collection = client['newsfilter'].news

@socketio.on('label')
def handle_label(data):
    collection.update_one({ '_id': data['_id']}, {'$set': {'label': data['label']}})

@app.route('/articles')
def get_articles():
    cursor = collection.find({ 'label': None }, limit=20).sort('added', ASCENDING)
    return dumps(cursor)

def run():
    socketio.run(app, '0.0.0.0')
