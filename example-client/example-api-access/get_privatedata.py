import nacl.secret
import nacl.utils
import nacl.signing
import json
import base64
import urllib.request
import nacl.pwhash


url = "http://cs302.kiwi.land/api/get_privatedata"

username = 'tche562'
password =  'tche562_310725746'

passw = "panima"
passwo = passw * 16
PNM = passwo[:16].encode('utf-8')

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
print(JSON_object)

#derive a symmetric key.
key = nacl.pwhash.argon2i.kdf(32,passw.encode('utf-8'),PNM, 8, 536870912)

#create a random nonce
nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

box = nacl.secret.SecretBox(key)

encrypted_base64_str = JSON_object['privatedata']

decrypted_base64 = base64.b64decode(encrypted_base64_str)

decrypted = box.decrypt(decrypted_base64)

plaintext = json.loads(decrypted.decode('utf-8'))

pw = plaintext['privatedata']

print(pw)
print("----------------------------")
