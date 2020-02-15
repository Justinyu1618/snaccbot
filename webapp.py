from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['snaccbot']
requests = db['requests']

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/delivery', methods=['GET', 'POST'])
def delivery():
    if request.method == 'GET':
        pass
    else:
        pass

@app.route('/slackbot', methods=['POST'])
def slackbot():
    print(request)
    return request.json['challenge']


app.run(port=3000, debug=True)
