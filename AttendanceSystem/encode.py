import cv2
import face_recognition
import os
import pickle

# Encoding Image to be understandable by Model
path = 'images'
images = [] 
ucid = []
myList = os.listdir(path)
# print(myList)

for img in myList: 										# Reading Each Array from Folder
	currentImg = cv2.imread(f'{path}/{img}')			# Read images in BGR color format (of each pixel)
	images.append(currentImg)
	ucid.append(os.path.splitext(img)[0])				# Seperates file name & file extension
# print(ucid)

encodeList = []
i=1
for img in images:
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)			# Convert images from BGR to RGB color format
	encode = face_recognition.face_encodings(img)[0]	# Converts image pixel data to relevant data (128 dimension) for the model
	print('Encoding.. ', i, '/', len(images), sep='')	# Prints progress
	encodeList.append(encode)
	i+=1

print('All Encodings Complete!')

with open('encodeList.bat', 'wb') as f:					# Creates/Overrides the binary file 'encodeList.bat' for dumping
	pickle.dump([encodeList, ucid], f)					# Dump binary data of the encoded images