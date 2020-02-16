from flask import Flask, render_template, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests

app = Flask(__name__)
app.config.from_json('config.json')

client = MongoClient('localhost', 27017)
db_requests = client['snaccbot']['requests']

nodes = {
    'A': (0, 0),
    'B': (2, 2),
    'C': (1, 2),
    'D': (0, 2)
}

edges = {
    'A': ['B', 'D'],
    'B': ['C'],
    'C': [],
    'D': ['C']
}

root = 'A'
cur_request_id = None

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', requests=db_requests.find({'complete': False}), cur_request=db_requests.find_one({'_id': cur_request_id}))

@app.route('/send', methods=['POST'])
def send():
    global cur_request_id
    if cur_request_id is None:
        cur_request_id = ObjectId(request.form['request_id'])
        return 'success'
    else:
        return 'previous delivery not yet complete', 400

@app.route('/mark_home', methods=['POST'])
def mark_home():
    global cur_request_id
    cur_request_id = None
    return 'success'

@app.route('/mark_complete', methods=['POST'])
def mark_complete():
    request_id = request.form['request_id']
    print(request_id)
    db_requests.find_one_and_update({'_id': ObjectId(request_id)}, {'$set': {'complete': True}})
    return 'success'

@app.route('/snaccbot/graph', methods=['GET'])
def snaccbot_graph():
    """Get graph"""
    return {
        'nodes': nodes,
        'edges': edges,
        'root': root
    }

@app.route('/snaccbot/node', methods=['GET'])
def snaccbot_node():
    """Get node that snaccbot should be going to rn"""
    if cur_request_id is None:
        return root
    r = db_requests.find_one({'_id': cur_request_id})
    if r['complete']:
        return root
    return r['node']

def send_message(message, channel):
    return requests.post('https://slack.com/api/chat.postMessage', data={
        'token': app.config['SLACKBOT_TOKEN'],
        'channel': channel,
        'text': message
    })

@app.route('/slackbot', methods=['POST'])
def slackbot():
    if 'challenge' in request.json:
        return request.json['challenge']
    event = request.json['event']
    if event['type'] == 'message' and 'bot_id' not in event:
        text = event['text']
        try:
            node, item = text.split(' ', 1)
            if node not in nodes:
                send_message(f'{node} is not a valid node', event['channel'])
            else:
                resp = send_message(f'Sending {item} to {node}! Please thumbs up this message once you\'ve received your snacc', event['channel']).json()
                print('resp', resp)
                db_requests.insert_one({
                    'node': node,
                    'item': item,
                    'user': event['user'],
                    'complete': False,
                    'ts': resp['ts']
                })
        except Exception as e:
            print('error', e)
            send_message('Please format message as <location_id> <request>', event['channel'])
        return 'success'
    if event['type'] == 'reaction_added' and event['reaction'] == '+1':
        ts = event['item']['ts']
        db_requests.find_one_and_update({'ts': ts}, {'$set': {'complete': True}})
        return 'success'
    print('unhandled', request.json)
    return 'not implemented'

app.run(port=3000, debug=True)
