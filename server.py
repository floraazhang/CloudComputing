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
sys.path.append("database/")
import db




async_mode = None
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)




# @socketio.on('connect', namespace='/test_conn')
# def test_connect():
#     while True:
#         socketio.sleep(5)
#         t = ["江泽民","薄熙来","习近平"]
#         T=t[random.randint(0,2)]
#         print(T)
#         socketio.emit('server_response', {'data': T}, namespace='/test_conn')
 

@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('my response', {'data': 'Connected'}, namespace='/chat')
 



@socketio.on('message',namespace='/test_conn')
def test_emit(message):
    print(message)
    #socketio.emit('myEvent',"Chongqing",namespace='/test_conn')
    i=0
    while True:
        
        t = ["打黑除恶","我有思想准备","是要触及一些人的利益","是会触及一些人的利益","是会有，不同的观点和看法的"]

        data=db.getdata()

        print(data)
        
        socketio.sleep(3)

        socketio.emit('server_response', {'data': t[i]}, namespace='/test_conn')
        i+=1
        if i==5:
            i=0

        socketio.emit('cow_data', data, namespace='/test_conn')
        

    
    


 
def ack():
    print("message received!")


@app.route("/")
def api_index():

    return send_from_directory('./','tables-data-new.html')




if __name__ == '__main__':
	socketio.run(app)

    
    



