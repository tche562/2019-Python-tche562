import sqlite3
import nacl.signing
import nacl.encoding

username= "tche562"
password = "tche562_310725746"

tablename = 'ol_user_info'
 
# Generate a new random private key
mypriv_k = nacl.signing.SigningKey.generate()

# transfer priv into hex_str
hex_str_mypriv_k = mypriv_k.encode(encoder=nacl.encoding.HexEncoder).decode('utf-8')

# Obtain the public key for a given private key
mypub_k = mypriv_k.verify_key

# transfer pub into hex_str
hex_str_mypub_k = mypub_k.encode(encoder=nacl.encoding.HexEncoder).decode('utf-8')

# Sign a signature with the signing key
mysig = bytes(hex_str_mypub_k+username,encoding='utf-8')

signed = mypriv_k.sign(mysig,encoder=nacl.encoding.HexEncoder)

hex_str_mysig = signed.signature.decode('utf-8')

con = sqlite3.connect('database.db')
c = con.cursor()

c.execute("INSERT INTO USER_INFO(name,privatekey,publickey,signature,password)\
        VALUES('"+username+"','"+hex_str_mypriv_k+"','"+hex_str_mypub_k+"','"+hex_str_mysig+"','"+password+"')");

con.commit()

con.close()

def delete_db(tablename):
        con = sqlite3.connect('database.db')
        c = con.cursor()
        c.execute("DELETE from "+tablename)
        con.commit()
        con.close()