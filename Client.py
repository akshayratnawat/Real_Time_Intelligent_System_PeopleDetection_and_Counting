# Importing the required libraries
import socket
import sys
import cv2
import pickle
import numpy as np
import struct

# Initializing the Histogram of Oriented Gradients for Human Detection from OpenCV
HOGCV = cv2.HOGDescriptor()

# Calling a pre-trained SVM Model for Human Detection 
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Everything will be done by detectMultiScale(). It returns 2-tuple.

# List containing Coordinates of bounding Box of person.
# Coordinates are in form X, Y, W, H.
# Where x,y are starting coordinates of box and w, h are width and height of box respectively.
# Confidence Value that it is a person.


# Creating a function to detect people in each frame of the video
def detect(frame):

	# DetectMultiscale function of HOGCV returns the Coordinates of the Box (x-cordinate, y-cordinate, Height(h), width(w) )
	bounding_box_cordinates, weights =  HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)
	
	person = 1
	
	# The first element in the tuple is a list
	# that contains coordinates of bounding box of person
	# Coordinates are in form X, Y, W, H.
	# Where x,y are starting coordinates of box and w, h are width and height of box respectively.
	# Running a loop over all the coordinates given by Model
	for x,y,w,h in bounding_box_cordinates:
		
		# Creating a Rectangular Frame using those coordinates
		cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

		# Using the text function to show the counter of people, detector in each frame
		cv2.putText(frame, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
		person += 1
	
	cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
	cv2.putText(frame, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)

	# Showing each frame
	#cv2.imshow('frame', frame)

	return frame

# Creatign a definition to increase the size of image while at the same time maintaining the aspect ratio of the image
def display(img, frameName="OpenCV Image"):
    h, w = img.shape[0:2]
    new_width = 1600
    new_height = int(new_width*(h/w))
    img = cv2.resize(img, (new_width, new_height))
    cv2.imshow(frameName, img)
    cv2.waitKey(1)


# Storing the Host and Port
HOST = '192.168.0.137'
PORT = 9996

# Creating a socket 
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# Bind the socket with designated HOST and PORT
s.bind((HOST, PORT))

# Print to confirm binding status
print('Socket bind complete')

# Socket to listen for signals 
s.listen(10)

# Print to confirm listening status
print('Socket now listening')

# Printing the Connection and Address from where the server is accepting the data
conn, addr = s.accept()

# Initializing the payload size and storing it into payload_size variable
data = b''
payload_size = struct.calcsize("L")


while True:

	# Message contains the length of data in front of the data itself. So Extracting the length of data from the whole string of data
	while len(data) < payload_size:

		# Receiving the data till we receive the whole value for the length of data
		data += conn.recv(4096)

	# Finding the size of the message  
	packed_msg_size = data[:payload_size]

	# The actual frame data starts after the payload size value and afterwards
	data = data[payload_size:]

	# Storing the size of the message into a variable
	msg_size = struct.unpack("L", packed_msg_size)[0]

	# Looping over and receiving more data if the length of data is less than the message size
	while len(data) < msg_size:
		data += conn.recv(4096)
	
	# Once it receives the complete data for a particular frame, storing it into a variable called frame_data
	frame_data = data[:msg_size]

	# Updating the data variable after the message size to receive the next frame
	data = data[msg_size:]

	# Loading the pickled data into its original form
	frame=pickle.loads(frame_data)
	#print(frame.size)

	# Showing the frame after applying the detect function on the frame
	# cv2.imshow('frame', detect(frame))
	# cv2.waitKey(1)
	display(detect(frame) )



