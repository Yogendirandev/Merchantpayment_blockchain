import sqlite3

conn = sqlite3.connect("user.db")
c = conn.cursor()
userid="user3"
c.execute("DELETE  FROM user WHERE username=?", (userid,))
c.execute("select * from user")
conn.commit()
print(c.fetchall())