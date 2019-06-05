import sqlite3
import nacl.signing
import nacl.encoding

rec = 'fhakdhf1231'
un = 'tche562'

con = sqlite3.connect('database.db')
c = con.cursor()
c.execute("UPDATE USER_INFO set record = '"+rec+"' where name = '"+un+"'")

con.commit()