from flask import Flask
from flask_socketio import SocketIO
from pymongo import MongoClient, ASCENDING
from bson.json_util import dumps

app = Flask(__name__)
socketio = SocketIO(app)
client = MongoClient()
collection = client['newsfilter'].alerts

@socketio.on('label')
def handle_label(data):
    collection.update_one({ '_id': data['_id']}, {'label': data['label']})
    print 'holla'
    print data

@app.route('/articles')
def get_articles():
    cursor = collection.find({ 'label': None }, limit=20).sort('added', ASCENDING)
    return dumps(cursor)

def run():
    socketio.run(app)
