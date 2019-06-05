import urllib.request
import json
import base64

# url = "http://cs302.kiwi.land/api/ping"
url = 'http://172.23.78.194:1234/api/rx_broadcast'


#STUDENT TO UPDATE THESE...
username = "tche562"
password = "tche562_310725746"

#create HTTP BASIC authorization header
credentials = ('%s:%s' % (username, password))
b64_credentials = base64.b64encode(credentials.encode('ascii'))
headers = {
    'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
    'Content-Type' : 'application/json; charset=utf-8',
}

payload = {
    "connection_location": "2", 
    "connection_address": "0.0.0.0.1234"
}


payload_json = json.dumps(payload)
payload_byte = payload_json.encode('utf-8')

try:
    req = urllib.request.Request(url, payload_byte)
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

