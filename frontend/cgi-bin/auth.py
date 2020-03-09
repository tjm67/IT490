#!/usr/bin/python
import pika
import time
from flask import request
import cgi, cgitb

time.sleep(2)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='messaging'))
channel = connection.channel()
channel.queue_declare(queue='auth')

form = cgi.FieldStorage()
email = form.getvalue('email')
psw = form.getvalue('psw')
print "Content-type: text/html \n"

channel.basic_publish(exchange='', routing_key='hello', body=email)

connection.close()