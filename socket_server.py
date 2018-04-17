from flask import Flask, render_template,request
from flask_socketio import SocketIO
import time
import logging

logging.getLogger('socketio').setLevel(logging.ERROR)
app = Flask(__name__)

socketio = SocketIO(app,logger= False,log_output=False)
@socketio.on('connect')
def connect():
    
    print 'Connected'+request.namespace
    
@socketio.on('disconnect')
def disconnect():
    
    print 'Disconnected'
@socketio.on('update pos',namespace="/qpy")
def handle_query(dim):
	
	socketio.emit("new pos",dim,namespace="/web")
	

    
if __name__ == '__main__':
    socketio.run(app,host='localhost',port=8001,debug=False)