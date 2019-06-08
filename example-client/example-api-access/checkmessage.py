import urllib.request
import json
import base64
import nacl.signing
import nacl.encoding
import sqlite3
import time 
import binascii
import db_setup
import cherrypy

def checkmessage(username):

    fl_ts = db_setup.get_outtime(username)
    ts = str(fl_ts)

    user,_,address,status = db_setup.get_chatmate_info()


    con = sqlite3.connect('database.db')
    c = con.cursor()
    cursor = c.execute("SELECT name,password from USER_INFO")
    for row in cursor:
            if username == row[0]:
                password = row[1]
    con.close()

    # for index in range(len(user)):
    #     if status[index] != "offline" :
    #         p_address = address[index]
    url = "http://10.0.0.16:10009/api/checkmessages?since="+ts


    #create HTTP BASIC authorization header
    credentials = ('%s:%s' % (username, password))
    b64_credentials = base64.b64encode(credentials.encode('ascii'))
    headers = {
        'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
        'Content-Type' : 'application/json; charset=utf-8',
    }


    try:
        req = urllib.request.Request(url,  headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read() # read the received bytes
        encoding = response.info().get_content_charset('utf-8') #load encoding if possible (default to utf-8)
        response.close()
    except urllib.error.HTTPError as error:
        print(error.read())
        exit()

    JSON_object = json.loads(data.decode(encoding))
    print("-------------------------showing response from checkmessage----------")
    print(JSON_object)

checkmessage("tche562")