import numpy as np
import urllib
import cv as cv2
from time import sleep
import sys
from PIL import Image
import socket
import androidhelper.sl4a as android
from StringIO import StringIO
import urllib
from socketIO_client import SocketIO, LoggingNamespace
from time import sleep
import threading
qpy_namespace = None
scaling_factor=10
def on_connect():
    print('connect')
def on_reconnect():
    print('reconnect')
def on_disconnect():
    print('disconnect')
#set ip, socket port and camera port
ip=192.168.43.1
socket_port=8001
camera_port=8081
def url_to_image():
	url = "http://"+ip+":"+camera_port+"/shot.jpg"
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	res = urllib.urlopen(url)
	image = np.asarray(bytearray(res.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	# perform the actual resizing of the image according to scaling_factor
	height, width = image.shape[:2]
	resized = cv2.resize(image, (width/scaling_factor, height/scaling_factor), interpolation = cv2.INTER_AREA)
	# Return gray sale image
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	return gray
# Set the haarcascade file path
cascPath = "haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# Open a flask connection to sl4a server to send information to takser
# If your QPython is able to send messages to tasker directly use script version v2
with SocketIO(ip, port) as socketIO:
	qpy_namespace = socketIO.define(LoggingNamespace, '/qpy')
	socketIO.on('connect', on_connect)
	socketIO.on('reconnect', on_reconnect)
	socketIO.on('disconnect', on_disconnect)
	
	
	
	
	def recognition():
		while True:
			# Get frame from video
			image = url_to_image()
			# Detect faces in the image
			faces = faceCascade.detectMultiScale(
    			image,
    			scaleFactor=1.2,
    			minNeighbors=5,
    			minSize=(10, 10),
    			flags = cv2.cv.CV_HAAR_SCALE_IMAGE
			)
			# Print result
			print("Found {0} faces!".format(len(faces)))
	
			# Draw a rectangle around the faces
			
			dim=[]
			for (x, y, w, h) in faces:
				
				# push x,y,w,h to dim
				dim.push(str(w*scaling_factor)+","+str(h*scaling_factor)+","+str(x*scaling_factor)+","+str(y*scaling_factor))
				
			# Send to server
			qpy_namespace.emit("update pos","|".join(dim))
				
				
			
		
	def listener():
		socketIO.wait()
		
		
		
		
# Threading to send and receive messages from sl4a
recognizer= threading.Thread(name='recognition', target=recognition)
listener = threading.Thread(name='listener', target=listener)

recognizer.start()
listener.start()
	
	
