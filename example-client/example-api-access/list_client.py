import urllib.request
import json
import base64
import sqlite3

username = 'tche562'



url = "http://cs302.kiwi.land/api/list_users"

con = sqlite3.connect('database.db')
c = con.cursor()
cursor = c.execute("SELECT name,password from USER_INFO")
for row in cursor:
        if username == row[0]:
            password = row[1]

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


