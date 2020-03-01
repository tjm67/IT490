import psycopg2, time
time.sleep(5)

conn = None
try:
	conn = psycopg2.connect(host="it490_postgres_1",database="mydb",user="root",password="root")
	cur = conn.cursor()
	cur.execute("SELECT * from users;")
	print("Number of users: ", cur.rowcount)
	cur.execute("INSERT INTO users VALUES ('anthony joshua', DEFAULT, 'pass');")
	cur.execute("SELECT * from users;")
	print("Number of users: ", cur.rowcount)
	cur.close()
except (Exception, psycopg2.DatabaseError) as error:
        print(error)
finally:
	if conn is not None:
		conn.close()