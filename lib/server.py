from __future__ import print_function
from flask import Flask, request
from flask_socketio import SocketIO
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.json_util import dumps
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup
from toolz import assoc_in
import os
import sys
import datetime as dt


# Make app
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# Connect to Mongo --> TODO: close connection on shutdown hook!
client = MongoClient(
    host = os.environ.get('MONGO_HOST') or None
)


def days_ago(days):
    return dt.datetime.utcnow() - dt.timedelta(days = days)

@socketio.on('label')
def handle_label(data):
    collection = client['newsfilter'].news

    # update every items within the cluster!!
    doc = collection.find_one({'_id': data['_id']})
    cluster = doc.get('cluster')
    if cluster:
        collection.update_many({ 'cluster': cluster}, {'$set': {'label': data['label']}})


@app.route('/terms')
def get_sources():
    collection = client['newsfilter'].terms
    cursor = collection.find()
    return dumps(cursor)

# Grab cluster of article and get 20 similar articles...
@app.route('/cluster/<cluster>')
def get_cluster(cluster):
    cluster = int(cluster)
    collection = client['newsfilter'].news
    cursor = collection.find({'cluster': cluster})
    return dumps(cursor[0:30])


@app.route('/articles/')
def get_articles():
    collection = client['newsfilter'].news
    start = int(request.args.get('start')) or 0
    label = request.args.get('label') or None
    days = int(request.args.get('days')) or 10

    cursor = collection.aggregate([
        { '$match': { 'label': label, 'added': { '$gt': days_ago(days) } }},
        { '$sort': { 'prediction': 1, 'published': 1 }},
        { '$group': { '_id': '$cluster', 'item': { '$first': '$$ROOT' }}}
    ])
    # get similar
    l = list(cursor)[start: start+20]
    return dumps(map(lambda x: x['item'] , l))

def run():
    socketio.run(app, '0.0.0.0')
