#!/usr/bin/env python
import pika
import time
import psycopg2

time.sleep(10)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='it490_messaging_1'))
channel = connection.channel()

channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

time.sleep(25)

conn = None
try:
	conn = psycopg2.connect(host="it490_postgres_1",database="mydb",user="root",password="root")
	cur = conn.cursor()
	
	cur.execute("CREATE TABLE IF NOT EXISTS users (name varchar(50) NOT NULL, id SERIAL, password varchar(30) NOT NULL);")
	cur.execute("SELECT * from users;")
	print("Number of users: ", cur.rowcount)
	cur.execute("INSERT INTO users VALUES ('anthony', DEFAULT, 'pass');")
	conn.commit()
	cur.execute("SELECT * from users;")
	print("Number of users: ", cur.rowcount)
	print(cur.fetchall())
	cur.close()
	
except (Exception, psycopg2.DatabaseError) as error:
        print(error)
finally:
	if conn is not None:
		conn.close()
