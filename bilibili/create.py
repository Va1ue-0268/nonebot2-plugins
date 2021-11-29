import sqlite3


conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute('''CREATE TABLE bilibili
    (gid INTEGER not null,
    mid INTEGER not null,
    name char(50),
    live INTEGER,
    dynamic INTEGER,
    latest_dynamic INTEGER,
    primary key(gid, mid));''')
conn.commit()
conn.close()