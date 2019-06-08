import urllib.request
import json
import base64
import nacl.signing
import nacl.encoding
import sqlite3
import get_IP
import cherrypy

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
  
    c.execute("UPDATE USER_INFO set record = '"+JSON_object['loginserver_record']+"' where name = '"+username+"'")
    con.commit()
    con.close()




def keytest(username):

    url = "http://cs302.kiwi.land/api/ping"


    con = sqlite3.connect('database.db')
    c = con.cursor()
    cursor = c.execute("SELECT name,publickey,signature,password from USER_INFO")
    for row in cursor:
            if username == row[0]:
                hex_str_mypub_k = row[1]
                hex_str_mysig = row[2]
                password = row[3]
    con.close()
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





def report(username,status):
    url = "http://cs302.kiwi.land/api/report"

    ip = cherrypy.server.socket_host+":"+str(cherrypy.server.socket_port)

    con = sqlite3.connect('database.db')
    c = con.cursor()
    cursor = c.execute("SELECT name,publickey,password from USER_INFO")
    for row in cursor:
            if username == row[0]:
                hex_str_mypub_k = row[1]
                password = row[2]
    con.close()
    #create HTTP BASIC authorization header
    credentials = ('%s:%s' % (username, password))
    b64_credentials = base64.b64encode(credentials.encode('ascii'))
    headers = {
        'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
        'Content-Type' : 'application/json; charset=utf-8',
    }

    payload = {
        "connection_address": ip,
        "connection_location": 2, 
        "incoming_pubkey": hex_str_mypub_k,
        "status": status
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

def list_user(username):
    url = "http://cs302.kiwi.land/api/list_users"

    con = sqlite3.connect('database.db')
    c = con.cursor()
    cursor = c.execute("SELECT name,password from USER_INFO")
    for row in cursor:
            if username == row[0]:
                password = row[1]

    con.close()
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

    JSON_object = json.loads(data.decode(encoding))
    inside = JSON_object['users']
    print(inside)


    con = sqlite3.connect('database.db')
    c = con.cursor()
    c.execute("UPDATE OL_USER_INFO set status = 'offline'")
    for user in inside:
        username = user['username']
        in_pubkey = user['incoming_pubkey']
        con_addr = user['connection_address']
        con_loc  = user['connection_location']
        con_up_at = user['connection_updated_at']
        status = user['status']
        print(username+"----------"+in_pubkey)
        try:
            c.execute("INSERT INTO OL_USER_INFO(username,publickey,address,status)\
            VALUES('"+username+"','"+in_pubkey+"','"+con_addr+"','"+status+"')")
            con.commit() 
        except:
            c.execute("UPDATE OL_USER_INFO set publickey = '"+in_pubkey+"', address = '"+con_addr+"', status = '"+status+"' where username = '"+username+"'")
            con.commit()
            
    con.close()






        




    
