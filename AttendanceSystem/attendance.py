import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pickle
import mysql.connector
import sys

cwd = '../AttendanceSystem'

MYSQLPASSWORD = open(os.path.join(cwd,'.env')).read()[6:]
Connection = mysql.connector.connect(username='admin', password=MYSQLPASSWORD, database='FaceTrack')

cursor = Connection.cursor()            # Connecting MySQL Database

date = datetime.today().date()          # Current date

year = date.year
month = date.month
day = date.day
TableName = '_' + str(year) + '_' + ('0'+str(month))[-2:] + '_' + str(day)

query = """CREATE TABLE IF NOT EXISTS {TableName}(
    SrNo INT PRIMARY KEY,
    UID CHAR(10),
    Name VARCHAR(30),
    Time TIME,
    Lecture INT NOT NULL
);""".format(TableName=TableName)       # Creates Table in Database 

cursor.execute(query)

args = sys.argv
if len(args) > 1:
    lecNo = int(args[1])
else:
    lecNo = input("Enter Lecture Number: ")                     # Input lecture number

with open(os.path.join(cwd,'encodeList.bat'), 'rb') as f:       # Reads the binary file
    data = pickle.load(f)                                       # Encoded data loaded
encodeListKnown = data[0]
ucid = data[1]

query = """SELECT UID, Lecture FROM {TableName};""".format(TableName=TableName)
cursor.execute(query)                                           # Fetch UID, Lecture
nameList = list(cursor.fetchall())

dictionary = {}

with open(os.path.join(cwd,'ucid.csv')) as f:
    for i in f.readlines():
        data = i.split(',')
        dictionary[data[0]] = data[1][:-1].title()
# print(dictionary)
l = len(nameList)
prevUCID = ''
n = 0
def attendance(ucid, frame, pos): # Marking The Attendance After Recognise A Person
    global l, lecNo, prevUCID, n
    if (prevUCID == ucid):
        n+=1
    else:
        prevUCID = ucid
        n=0
    if (n>=8):
        if (ucid, lecNo) not in nameList:
            time_now = datetime.now()
            tStr = time_now.strftime('%H:%M:%S')
            query = """INSERT INTO {TableName} VALUES ({SrNo}, "{UID}", "{Name}", "{Time}", {Lecture});""".format(TableName=TableName, SrNo=len(nameList)+1, Name=dictionary[ucid], UID=ucid, Time=tStr, Lecture=lecNo)
            cursor.execute(query)
            Connection.commit()
            nameList.append((ucid, lecNo))
            print("Attendance Marked", dictionary[ucid])

        cv2.rectangle(frame, (pos['x1'], pos['y1']), (pos['x2'], pos['y2']), (0, 255, 0), 2)
        cv2.rectangle(frame, (pos['x1'], pos['y2'] - 35), (pos['x2'], pos['y2']), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, dictionary[name].upper(), (pos['x1'] + 6, pos['y2'] - 6), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
        l+=1
    else:
        cv2.rectangle(frame, (pos['x1'], pos['y1']), (pos['x2'], pos['y2']), (0, 0, 255), 2)
        cv2.rectangle(frame, (pos['x1'], pos['y2'] - 35), (pos['x2'], pos['y2']), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, 'INDENTIFYING...', (pos['x1'] + 6, pos['y2'] - 6), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

    facesCurrentFrame = face_recognition.face_locations(faces)
    encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

    for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = ucid[matchIndex]
            # print(dictionary[name])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            pos = {'x1':x1, 'y1':y1, 'x2':x2, 'y2':y2}
            

            # cv2.putText(frame, dictionary[name].upper(), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
            attendance(name, frame, pos)

    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) == 13:
        break

cap.release()
cv2.destroyAllWindows()


Connection.commit()
Connection.close()