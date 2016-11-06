from flask import Flask
from flask_socketio import SocketIO
from pymongo import MongoClient, ASCENDING
from bson.json_util import dumps
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

client = MongoClient(
    host = os.environ.get('MONGO_HOST') or None
)
collection = client['newsfilter'].alerts

@socketio.on('label')
def handle_label(data):
    print data
    collection.update_one({ '_id': data['_id']}, {'$set': {'label': data['label']}})

@app.route('/articles')
def get_articles():
    print 'get articles!!!'
    cursor = collection.find({ 'label': None }, limit=20).sort('added', ASCENDING)
    return dumps(cursor)

def run():
    socketio.run(app, '0.0.0.0')
