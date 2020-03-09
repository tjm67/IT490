#!/usr/bin/env python
import pika
import time
import psycopg2

time.sleep(25)

conn = None
try:
	conn = psycopg2.connect(host="postgres",database="mydb",user="root",password="root")
	cur = conn.cursor()
	print(cur.fetchall())


except (Exception, psycopg2.DatabaseError) as error:
        print(error)
finally:
	if conn is not None:
		conn.close()
