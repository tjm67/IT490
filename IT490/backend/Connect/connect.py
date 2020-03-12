#!/usr/bin/env python
import pika
import time
import psycopg2
import json
from werkzeug.security import generate_password_hash, check_password_hash

time.sleep(15)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='messaging'))
channel = connection.channel()

channel.queue_declare(queue='register')
channel.queue_declare(queue='login')

print(' [*] Waiting for messages. To exit press CTRL+C')

def loginCallback(ch, method, properties, body):

    jsonMsg = json.loads(body)

    print(jsonMsg)
    
    email = jsonMsg['email']
    password = jsonMsg['password']    
    
    try:
        conn = psycopg2.connect(host="postgres",database="mydb",user="root",password="root")
        cursor = conn.cursor()
        postgres_select_query = """SELECT password FROM users WHERE email = %s"""
        
        cursor.execute(postgres_select_query, (email,))

        count = cursor.rowcount
        print (count, "Record returned successfully frrom users table")
        
        check_pass = cursor.fetchone()[0]
        
        if(check_password_hash(check_pass, password)):
            # return a boolean from the callback function to the frontend telling it the result of the login.
        
            print("LOGIN Success")
        else:
            print("LOGIN FAILED")

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to select record from users table", error)

    finally:
        #closing database connection.
        if(conn):
            cursor.close()
            
    
    




def registerCallback(ch, method, properties, body):
    print(" [x] Received %r" % body)

    try:
        conn = psycopg2.connect(host="postgres",database="mydb",user="root",password="root")
        cursor = conn.cursor()
        postgres_insert_query = """INSERT INTO users (email, password) VALUES (%s,%s)"""
        
        jsonMsg = json.loads(body)
        record_to_insert = (jsonMsg['email'], generate_password_hash(jsonMsg['password']))
        cursor.execute(postgres_insert_query, record_to_insert)

        conn.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)

    finally:
        #closing database connection.
        if(conn):
            cursor.close()

channel.basic_consume(queue='register', on_message_callback=registerCallback, auto_ack=True)
channel.basic_consume(queue='login', on_message_callback=loginCallback, auto_ack=True)
channel.start_consuming()
