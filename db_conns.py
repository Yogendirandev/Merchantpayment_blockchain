import sqlite3



def login(userid, password):
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    c.execute(f"SELECT * FROM user WHERE username = '{userid}' AND password = '{password}'")
    num = c.fetchall()
    conn.commit
    conn.close()
    return num

def signup(userid, acc_addr, priv_key, password):
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    c.execute(f"INSERT INTO user VALUES ('{userid}', '{acc_addr}', '{priv_key}', '{password}')")
    conn.commit()
    conn.close()
    return 1

def getPrivateKey(userid):
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    c.execute(f"SELECT private_key FROM user WHERE username='{userid}'")
    privateKey = c.fetchall()[0][0]
    conn.close()
    return privateKey

def getAccountAddress(userid):
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    c.execute(f"SELECT account_address FROM user WHERE username='{userid}'")
    addr = c.fetchall()[0][0]
    conn.close()
    return addr

