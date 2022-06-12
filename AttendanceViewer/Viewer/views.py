from http.client import HTTPResponse
from re import L
from tokenize import Name
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

from subprocess import run,PIPE
import sys

import mysql.connector

# Create your views here.
def home(request, lec=0):
    date, lect = '', lec
    try:
        date = request.GET['date']
    except:
        date = str(datetime.today().date())
    if(not(date)): date = str(datetime.today().date())
    try:
        lect = request.GET['lect']  
    except:
        pass
    TableName = '_' + date.replace('-', '_')
        
    displayDate = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")

    Connection = mysql.connector.connect(username='admin', password='VineetMySQL25!', database='FaceTrack')

    cursor = Connection.cursor()

    
    if(not(lect)): 
        query =  """SELECT * FROM {TableName};""".format(TableName=TableName)
    else:
        query = """SELECT * FROM {TableName} WHERE Lecture = {Lect};""".format(TableName=TableName, Lect=lect)
    try:
        cursor.execute(query)
        DATA = cursor.fetchall()
    except:
        DATA = []

    Connection.close()

    DATA = list(map(lambda x: list(x), DATA))
    # print(DATA)
    rows = addRows(DATA)
    return render(request, 'base.html', {'displayDate': displayDate, 'rows': rows})

def addRows(DATA):
    j=1
    rows = ''
    for i in DATA:
        rows += """<tr><td>{SrNo}</td><td>{UID}</td><td>{Name}</td><td>{Time}</td><td>{Lecture}</td></tr>""".format(SrNo=j, UID=i[1], Name=i[2], Time=i[3], Lecture=i[4])
        j+=1
    
    return rows

def addRows_date(DATA):
    rows = ''
    for i in DATA:
        rows += """<tr><td>{SrNo}</td><td>{UID}</td><td>{Name}</td><td>{Date}</td><td>{Time}</td><td>{Lecture}</td></tr>""".format(SrNo=i[0], UID=i[1], Name=i[2], Date=i[3], Time=i[4], Lecture=i[5])
    
    return rows

def about(request):
    return render(request, 'about.html')

def ucidfilter(request):
    try:
        ucid = request.GET['ucid']
    except:
        ucid = 0
    Connection = mysql.connector.connect(username='admin', password='VineetMySQL25!', database='FaceTrack')
    cursor = Connection.cursor()

    query = """SHOW TABLES;"""
    cursor.execute(query)
    tables = cursor.fetchall()
    data = []
    for table in tables:
        query = """SELECT * FROM {TableName} WHERE UID='{ucid}'""".format(TableName=table[0], ucid=ucid)
        cursor.execute(query)
        d=[]
        for i in cursor.fetchall():
            d.append([i[0], i[1], i[2], table[0][1:].replace('_', '-'), i[3], i[4]])
        data+=d
    data = addRows_date(data)

    Connection.close()

    return render(request, 'ucidfilter.html', {'ucid': ucid, 'rows':data})

def archive(request):
    return render(request, 'archive.html')

def external(request):
    try:
        lect = request.GET['lect']
    except:
        lect = 1
    out = run([sys.executable, "C:/Users/vinee/Desktop/FaceTrack/AttendanceSystem/attendance.py", lect], shell=False, stdout=PIPE)
    return home(request, lect)