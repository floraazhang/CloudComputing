 #! /usr/bin/env python
# -*- coding: utf-8 -*-


__doc__ = """web server
"""

import json

import flask
from flask import Flask, request, send_from_directory, Response,render_template
from flask_socketio import SocketIO
from flask_cors import CORS

import random
import sys
sys.path.append("db/")
import db


async_mode = None
app = Flask(__name__, template_folder='public')
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)





# login
import flask_login as flask_login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'foo@bar.tld': {'password': 'secret'}}

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('login.html') 

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user






#Serve Static Index page
@app.route('/')
def api_index():
    return send_from_directory('public', 'Cow_data.html')

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

        socketio.sleep(0)
        

def ack():
    print("message received!")





@app.route('/search')
@flask_login.login_required
def search():
    return render_template('search.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    flask_login.logout_user()

    if flask.request.method == 'GET':
        return render_template('login.html')

    #The request method is POST (page is recieving data)
    email = flask.request.form['email']
    if flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


@app.route('/register')
def register():
    return render_template('register.html') 





if __name__ == '__main__':
	socketio.run(app)

    
    



