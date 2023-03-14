import mysql.connector as mc
conn = mc.connect(host='localhost',user='root',passwd='mysql123')
cursor = conn.cursor()  

# cursor.execute("CREATE DATABASE app_users")
cursor.execute("SHOW DATABASES")
dbs=cursor.fetchall()
for db in dbs:
    print(db)