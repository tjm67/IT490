from flask import Flask, render_template, request
import cgi, cgitb, time
import pika
app = Flask(__name__)

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/login/' )
def Login():
    return render_template('login.html')
<<<<<<< HEAD

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
=======
>>>>>>> parent of e81dee5... Add files via upload
	
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
	channel.queue_declare(queue='hello')
	form = cgi.FieldStorage()
	msg= email + " " + password
	channel.basic_publish(exchange='', routing_key='hello', body=msg)

	connection.close()
	return render_template("index.html")
	
if  __name__=='__main__':
	app.run(debug=True)
