import urllib.request
import nacl.pwhash
import time
import sqlite3
import json



con = sqlite3.connect('database.db')
c = con.cursor()
list_bw = []
cursor = c.execute("SELECT word from word_block")
for item in cursor:
    sensitive_w = item[0]
    list_bw.append(sensitive_w)

str_list_bw = repr(list_bw)
str_list_bw = str_list_bw.replace("'","''")


con = sqlite3.connect('database.db')
c = con.cursor()
privkey_list = []

privkey_list = []
cursor = c.execute("SELECT privatekey from user_info")
for item in cursor:
    current_privkey = item[0]
    privkey_list.append(current_privkey)

str_privkey_list = repr(privkey_list)
str_privkey_list = str_privkey_list.replace("'","''")

c.execute("INSERT INTO PRIVATE_DATA(prikeys,blocked_words,flag)\
    VALUES('"+str_privkey_list+"','"+str_list_bw+"','1')")
con.commit()
con.close()

