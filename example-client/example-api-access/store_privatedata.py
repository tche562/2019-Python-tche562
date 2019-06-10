import urllib.request
import nacl.pwhash
import time
import sqlite3
import json

#load the list from private_data in database 

con = sqlite3.connect('database.db')
c = con.cursor()
cursor = c.execute("SELECT prikeys,blocked_words from private_data")
for item in cursor:
    str_privkey_list = item[0]
    str_list_bw = item[1]

privkey_list = str_privkey_list.split(",")
list_bw = str_list_bw.split(",")
    
#add current private key in 
cursor = c.execute("SELECT privatekey from user_info")
for item in cursor:
    current_privkey = item[0]
    privkey_list.append(current_privkey)




c.execute("UPDATE PRIVATE_DATA SET prikeys = "+privkey_list+" WHERE FLAG ='1'")
con.commit()
con.close()
