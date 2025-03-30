import sqlite3

conn = sqlite3.connect("user.db")
c = conn.cursor()

c.execute(""" CREATE TABLE user(
                username text,
                account_address text,
                private_key text,
                password text
)""")

conn.commit()
conn.close()