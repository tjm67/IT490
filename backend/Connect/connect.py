#!/usr/bin/env python
import pika
import time
import psycopg2

time.sleep(18)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='messaging'))
channel = connection.channel()

channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

if body != "":
    try:
        conn = psycopg2.connect(host="postgres",database="mydb",user="root",password="root")
        cursor = conn.cursor()
        postgres_insert_query = """ INSERT INTO users (email, password) VALUES (%s,%s)"""
        record_to_insert = (body, body)
        cursor.execute(postgres_insert_query, record_to_insert)

        conn.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)

    finally:
            #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
