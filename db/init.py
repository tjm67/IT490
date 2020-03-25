import psycopg2, time
time.sleep(6)

conn = None
try:
	conn = psycopg2.connect(host="postgres",database="mydb",user="root",password="root")
	cur = conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS users (email varchar(50) NOT NULL, password varchar(150) NOT NULL);")
	conn.commit()
	cur.close()

except (Exception, psycopg2.DatabaseError) as error:
        print(error)
finally:
	if conn is not None:
		conn.close()

print("DB initialized!")
