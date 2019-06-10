import urllib.request
import nacl.pwhash
import nacl.secret
import nacl.utils
import nacl.signing
import json
import base64
import time
import sqlite3
def add_current_prikey():

    #load the list from private_data in database 
    con = sqlite3.connect('database.db')
    c = con.cursor()
    cursor = c.execute("SELECT prikeys from private_data where flag = '1'")
    for item in cursor:
        str_privkey_list = item[0]

    #str to list
    str_privkey_list = str_privkey_list[2:-2]
    privkey_list = str_privkey_list.split(",")
    for item in privkey_list:
        item = item[2:-2]
    

    #add current private key in 
    cursor = c.execute("SELECT privatekey from user_info")
    for item in cursor:
        current_privkey = item[0]
        privkey_list.append(current_privkey)

    #list to str to str suiting database
    str_privkey_list = repr(privkey_list)
    str_privkey_list = str_privkey_list.replace("'","''")

    #insert it into private_data in database
    c.execute("UPDATE PRIVATE_DATA SET prikeys = '"+str_privkey_list+"' WHERE FLAG ='1'")
    con.commit()
    con.close()



add_current_prikey()






def encrypt_add_privatedata(secret_password,username):
    con = sqlite3.connect('database.db')
    c = con.cursor()
    cursor = c.execute("SELECT prikeys,blocked_words from private_data where flag = '1' ")
    for item in cursor:
        str_privkey_list = item[0]
        str_list_bw = item[1]

    str_privkey_list = str_privkey_list[2:-2]
    privkey_list = str_privkey_list.split(",")
    list_bw = str_list_bw.split(",")

    # secret_password = "panima"

    secret_password_16 = secret_password * 16
    PNM = secret_password_16[:16].encode('utf-8')

    privatedata = {"prikeys": privkey_list,
    "blocked_pubkeys": ["...", "..."],
    "blocked_usernames": ["...", "..."],
    "blocked_words": list_bw,
    "blocked_message_signatures": ["...", "..."],
    "favourite_message_signatures": ["...", "..."],
    "friends_usernames": ["...", "..."]}

    #derive a symmetric key.
    key = nacl.pwhash.argon2i.kdf(32,secret_password.encode('utf-8'),PNM, 8, 536870912)

    #create a random nonce
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

    box = nacl.secret.SecretBox(key)



    payload = {
            "privatedata":privatedata
        }

    payload_json = json.dumps(payload)

    payload_byte = payload_json.encode('utf-8')

    encrypted = box.encrypt(payload_byte, nonce)

    encrypted_base64 = base64.b64encode(encrypted)

    encrypted_base64_str = encrypted_base64.decode('utf-8')

    print("-------------------------"+encrypted_base64_str+"--------------------")

    ts = str(time.time())

    url = "http://cs302.kiwi.land/api/add_privatedata"

    cursor = c.execute("SELECT name,publickey,privatekey,password,record from USER_INFO")
    for row in cursor:
        if username == row[0] :
            hex_str_mypub_k = row[1]
            hex_str_mypriv_k = row[2]
            password = row[3]
            log_rec = row[4]


    mypriv_k = nacl.signing.SigningKey(hex_str_mypriv_k,encoder=nacl.encoding.HexEncoder)

    mysig = bytes(encrypted_base64_str+log_rec+ts,encoding='utf-8')

    signed = mypriv_k.sign(mysig,encoder=nacl.encoding.HexEncoder)

    hex_str_mysig = signed.signature.decode('utf-8')

    #create HTTP BASIC authorization header
    credentials = ('%s:%s' % (username, password))
    b64_credentials = base64.b64encode(credentials.encode('ascii'))
    headers = {
        'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
        'X-signature': hex_str_mysig,
        'Content-Type' : 'application/json; charset=utf-8',
    }

    payload = {
        "privatedata" : encrypted_base64_str,
        "loginserver_record" : log_rec,
        "client_saved_at" : ts,
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

    JSON_object = json.loads(data.decode(encoding))
    print(JSON_object)











def decrypt_get_privatedata(secret_password,username):


    url = "http://cs302.kiwi.land/api/get_privatedata"

    con = sqlite3.connect('database.db')
    c = con.cursor()
    cursor = c.execute("SELECT name,publickey,privatekey,password from USER_INFO")
    for row in cursor:
        if username == row[0] :
            hex_str_mypub_k = row[1]
            hex_str_mypriv_k = row[2]
            password = row[3]

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




    secret_password_16 = secret_password * 16
    PNM = secret_password_16[:16].encode('utf-8')

    #derive a symmetric key.
    key = nacl.pwhash.argon2i.kdf(32,secret_password.encode('utf-8'),PNM, 8, 536870912)

    #create a random nonce
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

    box = nacl.secret.SecretBox(key)

    encrypted_base64_str = JSON_object['privatedata']

    decrypted_base64 = base64.b64decode(encrypted_base64_str.encode('utf-8'))

    decrypted = box.decrypt(decrypted_base64)

    plaintext = json.loads(decrypted.decode('utf-8'))

    pw = plaintext['privatedata']

    print(pw)
    print("----------------------------")



# encrypt_add_privatedata("panima","tche562")
# decrypt_get_privatedata("panima","tche562")

