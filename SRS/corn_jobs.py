import sqlite3
conn = sqlite3.connect('../db.sqlite3')
c = conn.cursor()

c.execute("SHOW TABLES")

c.close()