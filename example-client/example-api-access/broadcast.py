import urllib.request
import json
import base64
import nacl.signing
import nacl.encoding
import sqlite3
import time 

username = 'tche562' 
message = 'what are u doing now'

url = "http://192.168.40.129:1234/api/rx_broadcast"

ts = str(time.time())


con = sqlite3.connect('database.db')
c = con.cursor()
cursor = c.execute("SELECT name,publickey,privatekey,password,record from USER_INFO")
for row in cursor:
    if username == row[0] :
        hex_str_mypub_k = row[1]
        hex_str_mypriv_k = row[2]
        password = row[3]
        log_rec = row[4]

mypriv_k = nacl.signing.SigningKey(hex_str_mypriv_k,encoder=nacl.encoding.HexEncoder)

mysig = bytes(log_rec+message+ts,encoding='utf-8')

signed = mypriv_k.sign(mysig,encoder=nacl.encoding.HexEncoder)

hex_str_mysig = signed.signature.decode('utf-8')

#create HTTP BASIC authorization header
credentials = ('%s:%s' % (username, password))
b64_credentials = base64.b64encode(credentials.encode('ascii'))
headers = {
    'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
    'Content-Type' : 'application/json; charset=utf-8',
}





payload = {
    "loginserver_record" : log_rec,
    "message" : message,
    "sender_created_at" : ts,
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