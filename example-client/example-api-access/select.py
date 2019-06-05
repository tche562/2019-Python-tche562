import sqlite3
import nacl.signing
import nacl.encoding

username = 'tche562'

con = sqlite3.connect('database.db')
c = con.cursor()
cursor = c.execute("SELECT name,publickey,signature,password from USER_INFO")
for row in cursor:
    if username == row[0]:
        hex_str_mypub_k = row[1]
        hex_str_mysig = row[2]
        password = row[3]
print (username)
print (hex_str_mypub_k)
print (hex_str_mysig)
print (password)

