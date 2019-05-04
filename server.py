 #! /usr/bin/env python
# -*- coding: utf-8 -*-


__doc__ = """web server
"""

import json
from flask import Flask, request, send_from_directory, Response
from flask_socketio import SocketIO
import random

from flask_cors import CORS

import sys
sys.path.append("db/")
import db




async_mode = None
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#Serve Static Index page
@app.route('/')
def api_index():
    return send_from_directory('public', 'Cow_data.html')


@app.route('/search_cow',methods=['GET'])
def Search_cow():

    

    cowID=request.args.get('ID')

    

    

    data=db.search_cow_byID(int(cowID))


    return Response(json.dumps(data), mimetype='application/json')



    



#Serve Other Static Pages
@app.route('/public/<path:path>')
def render_static(page_name):
    return send_from_directory('public', path)

@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('my response', {'data': 'Connected'}, namespace='/chat')
 

@socketio.on('message',namespace='/test_conn')
def test_emit(message):
    print(message)
    i=0
    while True:

        data=db.getdata()
        
        socketio.emit('cow_data', data, namespace='/test_conn')

        socketio.sleep(3)
        

def ack():
    print("message received!")





if __name__ == '__main__':
	socketio.run(app)

    
    



