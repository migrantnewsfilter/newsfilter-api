from __future__ import print_function
from flask import Flask, request
from flask_socketio import SocketIO
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.json_util import dumps
from bson.son import SON
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup
from toolz import assoc_in
import os
import sys
import datetime as dt
import logging

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


@app.route('/terms', methods = ['GET'])
def get_sources():
    collection = client['newsfilter'].terms
    cursor = collection.find()
    return dumps(cursor)

@app.route('/terms', methods = ['POST'])
def add_source():
    data = request.json
    collection = client['newsfilter'].terms
    if data.get('feed'):
        collection.update_one({'_id': data['source']},
                              { '$addToSet': {'feeds': data['feed']}})
        return "term added"
    else:
        return "ummmm..." # TODO!!!!

@app.route('/terms/<source>/<path:term_id>', methods = ['DELETE'])
def delete_source(source, term_id):
    collection = client['newsfilter'].terms
    collection.update_one({'_id': source}, { '$pull': { 'feeds': term_id}})
    return "term removed"

# Grab cluster of article and get 20 similar articles...
@app.route('/cluster/<cluster>')
def get_cluster(cluster):
    collection = client['newsfilter'].news
    cursor = collection.find({'cluster': cluster})
    return dumps(cursor[0:30])


@app.route('/articles/')
def get_articles():

    collection = client['newsfilter'].news
    start = int(request.args.get('start')) or 0

    label = request.args.get('label')
    label = None if label == 'unlabelled' else label

    days = int(request.args.get('days')) or 10
    relevance = request.args.get('relevance') or 'true'

    if relevance == 'true':
        sort = SON([ ('prediction', 1), ('published', 1)])
    else:
        sort = SON([ ('published', 1), ('prediction', 1)])

    cursor = collection.aggregate([
        { '$match': { 'label': label, 'published': { '$gt': days_ago(days) } }},
        { '$sort': sort },
        { '$group': { '_id': '$cluster', 'item': { '$first': '$$ROOT' }}}
    ])

    # return entire list...
    l = list(cursor)[0: start+20]
    return dumps(map(lambda x: x['item'] , l))

def run():
    socketio.run(app, '0.0.0.0')
