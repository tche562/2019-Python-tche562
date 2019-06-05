import urllib.request
import json
import base64
import nacl.signing
import nacl.encoding
import sqlite3
import time 

username = 'tche562' 
message = 'get from database'
target_username = 'bpen264'




ts = str(time.time())

con = sqlite3.connect('database.db')
c = con.cursor()
cursor = c.execute("SELECT username, publickey,address from OL_USER_INFO")
for row in cursor:
    if target_username == row[0] :
        target_pubkey = row[1]
        address = row[2]

url = "http://"+address+"/api/rx_privatemessage"

print(target_pubkey)

b_message = message.encode('utf-8')
verifykey = nacl.signing.VerifyKey(target_pubkey, encoder=nacl.encoding.HexEncoder)
g_publickey = verifykey.to_curve25519_public_key()
sealed_box = nacl.public.SealedBox(g_publickey)
encrypted = sealed_box.encrypt(b_message, encoder=nacl.encoding.HexEncoder)
privmessage = encrypted.decode('utf-8')


con = sqlite3.connect('database.db')
c = con.cursor()
cursor = c.execute("SELECT name,privatekey,password,record from USER_INFO")
for row in cursor:
    if username == row[0] :
        hex_str_mypriv_k = row[1]
        password = row[2]
        log_rec = row[3]

mypriv_k = nacl.signing.SigningKey(hex_str_mypriv_k,encoder=nacl.encoding.HexEncoder)

mysig = bytes(log_rec+target_pubkey+target_username+privmessage+ts,encoding='utf-8')

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
    "target_pubkey" : target_pubkey,
    "target_username" : target_username,
    "encrypted_message" : privmessage,
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