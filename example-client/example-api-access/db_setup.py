import sqlite3
import nacl.signing
import nacl.encoding


def generate_k(username, password) :
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
            VALUES('"+username+"','"+hex_str_mypriv_k+"','"+hex_str_mypub_k+"','"+hex_str_mysig+"','"+password+"')")

    con.commit()

    con.close()

def delete_db(tablename):
        con = sqlite3.connect('database.db')
        c = con.cursor()
        c.execute("DELETE from "+tablename)
        con.commit()
        con.close()

def get_chatmate_info():
        con = sqlite3.connect('database.db')
        c = con.cursor()
        username = []
        pubkey = []
        address = []
        status = []
        cursor = c.execute("SELECT username,publickey,address,status from OL_USER_INFO ORDER BY USERNAME")
        for row in cursor:
                username.append(row[0])
                pubkey.append(row[1])
                address.append(row[2])
                status.append(row[3])
        con.close()
        return username,pubkey,address,status


def get_chat_record():
        con = sqlite3.connect('database.db')
        c = con.cursor()
        sender = []
        ts = []
        content = []
        receiver = []
        payload = []
        cursor = c.execute("SELECT sender,time,content,receiver,payload from CHAT_RECORD ORDER BY TIME")
        for row in cursor:
                sender.append(row[0])
                ts.append(row[1])
                content.append(row[2])
                receiver.append(row[3])
                payload.append(row[4])
        con.close()
        return sender,ts,content,receiver,payload

def get_broadcast_record():
        con = sqlite3.connect('database.db')
        c = con.cursor()
        broadcaster = []
        ts = []
        content = []
        cursor = c.execute("SELECT broadcaster,time,content from BROADCAST_RECORD ORDER BY TIME DESC")
        for row in cursor:
                broadcaster.append(row[0])
                ts.append(row[1])
                content.append(row[2])
        con.close()
        return broadcaster,ts,content

def update_outtime(username,fl_ts):
        ts = str(fl_ts)
        con = sqlite3.connect('database.db')
        c = con.cursor()
        try:
                c.execute("INSERT INTO SIGNOUT_RECORD(username,out_time)\
                        VALUES('"+username+"','"+ts+"')")
                con.commit()
                con.close()
        except:
                c.execute("UPDATE SIGNOUT_RECORD SET OUT_TIME = "+ts+" WHERE USERNAME ='"+username+"'")
                con.commit()
                con.close()

def get_outtime(username):
        con = sqlite3.connect('database.db')
        c = con.cursor()
        try:
                cursor = c.execute("SELECT out_time from SIGNOUT_RECORD WHERE USERNAME ='"+username+"'")
                for item in cursor:
                        ts = item[0]
                con.commit()
                con.close()
                print(ts)
                print("---------------------------------------")
                return ts
        except:
                ts = 0
                print("++++++++++++++++++++++++++++++")
                print(ts)
                return ts





