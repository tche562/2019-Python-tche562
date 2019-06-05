import urllib.request
import json
import base64
import nacl.signing
import nacl.encoding
import sqlite3


def ping(username, password):
    url = "http://cs302.kiwi.land/api/ping"

    #create HTTP BASIC authorization header
    credentials = ('%s:%s' % (username, password))
    b64_credentials = base64.b64encode(credentials.encode('ascii'))
    headers = {
        'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
        'Content-Type' : 'application/json; charset=utf-8',
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read() # read the received bytes
        encoding = response.info().get_content_charset('utf-8') #load encoding if possible (default to utf-8)
        response.close()
    except urllib.error.HTTPError as error:
        print(error.read())
        exit()

    JSON_object = json.loads(data.decode(encoding))
    print(JSON_object)
    print(JSON_object['authentication'])
    return JSON_object


def addpubkey(username) :

    url = "http://cs302.kiwi.land/api/add_pubkey"

    con = sqlite3.connect('database.db')
    c = con.cursor()
    cursor = c.execute("SELECT name,publickey,signature,password from USER_INFO")
    for row in cursor:
        if username == row[0] :
            hex_str_mypub_k = row[1]
            hex_str_mysig = row[2]
            password = row[3]

    #create HTTP BASIC authorization header
    credentials = ('%s:%s' % (username, password))
    b64_credentials = base64.b64encode(credentials.encode('ascii'))
    headers = {
        'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
        'X-signature': hex_str_mysig,
        'Content-Type' : 'application/json; charset=utf-8',
    }





    payload = {
        "pubkey": hex_str_mypub_k,
        "username": username,
        "signature": hex_str_mysig
    }


    payload_json = json.dumps(payload)

    payload_byte = payload_json.encode('utf-8')

    try:
        req = urllib.request.Request(url, payload_byte, headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read() # read the received bytes
        encoding = response.info().get_content_charset('utf-8') #load encoding if possible (default to utf-8)
        response.close()
    except urllib.error.HTTPError as error:
        print(error.read())
        exit()

    JSON_object = json.loads(data.decode(encoding))
    print(JSON_object)

    #insert load from centre server to database
  
    c.execute("UPDATE USER_INFO set record = '"+JSON_object['loginserver record']+"' where name = '"+username+"'")
    con.commit()

def keytest(username):

    url = "http://cs302.kiwi.land/api/ping"


    con = sqlite3.connect('database.db')
    c = con.cursor()
    cursor = c.execute("SELECT username,publickey,signature,password from USER_INFO")
    for row in cursor:
            if username == row[0]:
                hex_str_mypub_k = row[1]
                hex_str_mysig = row[2]
                password = row[3]

    #create HTTP BASIC authorization header
    credentials = ('%s:%s' % (username, password))
    b64_credentials = base64.b64encode(credentials.encode('ascii'))
    headers = {
        'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
        'Content-Type' : 'application/json; charset=utf-8',
    }

    payload = {
        "pubkey": hex_str_mypub_k,
        "signature": hex_str_mysig
    }


    payload_json = json.dumps(payload)
    payload_byte = payload_json.encode('utf-8')

    try:
        req = urllib.request.Request(url, payload_byte, headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read() # read the received bytes
        encoding = response.info().get_content_charset('utf-8') #load encoding if possible (default to utf-8)
        response.close()
    except urllib.error.HTTPError as error:
        print(error.read())
        exit()

    JSON_object = json.loads(data.decode(encoding))
    return JSON_object

def report(username):
    url = "http://cs302.kiwi.land/api/report"

    con = sqlite3.connect('database.db')
    c = con.cursor()
    cursor = c.execute("SELECT name,publickey,password from USER_INFO")
    for row in cursor:
            if username == row[0]:
                hex_str_mypub_k = row[1]
                password = row[2]

    #create HTTP BASIC authorization header
    credentials = ('%s:%s' % (username, password))
    b64_credentials = base64.b64encode(credentials.encode('ascii'))
    headers = {
        'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
        'Content-Type' : 'application/json; charset=utf-8',
    }

    payload = {
        "connection_address": "0.0.0.0.1234",
        "connection_location": "2", 
        "incoming_pubkey": hex_str_mypub_k,
        "status": "online"
    }


    payload_json = json.dumps(payload)
    payload_byte = payload_json.encode('utf-8')

    try:
        req = urllib.request.Request(url,payload_byte, headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read() # read the received bytes
        encoding = response.info().get_content_charset('utf-8') #load encoding if possible (default to utf-8)
        response.close()
    except urllib.error.HTTPError as error:
        print(error.read())
        exit()

    JSON_object = json.loads(data.decode(encoding))
    print(JSON_object)
    print('report_ok')






        




    
