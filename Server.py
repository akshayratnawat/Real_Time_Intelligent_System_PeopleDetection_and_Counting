# Importing the required libraries
import cv2
import numpy as np
import socket
import sys
import pickle
import struct

# Starting the video 
cap = cv2.VideoCapture('video.mp4')

# Creating a client socket object
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting to the host and port (Server Socket) from the client socket
clientsocket.connect(('192.168.0.137', 9996))


while True:

	# Reading the frames from the videos
	ret,frame = cap.read()
	
	# Using pickle.dump to serialize the object and converting it into bytes object of the serialized object
	data = pickle.dumps(frame)

	# Sending the serialized object to the server. The message contains the length of data followed by the data itself
	clientsocket.sendall(struct.pack("L", len(data)) + data)