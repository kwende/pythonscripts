import sqlite3

conn = sqlite3.connect('coupons')

c = conn.cursor()
c.execute("insert into coupon values ('1', '2', '3', '5/26/1980')")

conn.commit()
conn.close()
