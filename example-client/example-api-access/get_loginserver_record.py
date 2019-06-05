import urllib.request
import json
import base64
import nacl.signing
import nacl.encoding
import sqlite3


username = 'tche562'
password = 'tche562_310725746'


url = "http://cs302.kiwi.land/api/get_loginserver_record"



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
print(JSON_object['loginserver_record'])

con = sqlite3.connect('database.db')
c = con.cursor()
c.execute("UPDATE USER_INFO set record = '"+JSON_object['loginserver_record']+"' where name = '"+username+"'")
con.commit()
con.close()