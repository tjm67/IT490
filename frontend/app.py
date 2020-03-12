from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
import cgi, cgitb, time
import pika
import json
app = Flask(__name__)

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def login_post():
    email = request.values.get('email')
    password = request.values.get('psw')
    
    # send pika message { email, password } to new queue 
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='messaging'))
    channel = connection.channel()
    channel.queue_declare(queue='login')
    form = cgi.FieldStorage()
    msgJson = { "email": email, "password": password }
    channel.basic_publish(exchange='', routing_key='login', body=json.dumps(msgJson))
    connection.close()

    # if result success:
    return render_template('profile.html')
    # else
    #    return render_template('login.html')
	
@app.route('/register/')
def register():
	return render_template('register.html')

@app.route('/register/', methods = ['POST'])	
def register_post():
    email = request.values.get('email')
    password = request.values.get('psw')
        
    time.sleep(2)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='messaging'))
    channel = connection.channel()
    channel.queue_declare(queue='register')
    form = cgi.FieldStorage()
    msgJson = { "email": email, "password": password }
    channel.basic_publish(exchange='', routing_key='register', body=json.dumps(msgJson))

    connection.close()
    return render_template("index.html")
    
 
if  __name__=='__main__':
	app.run(debug=True)
