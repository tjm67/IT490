from flask import Flask, render_template
app = Flask(__name__)

@app.route('/home/')
def Home():
    return render_template('index.html')

@app.route('/home/login/')
def Login():
    return render_template('login.html')
	
@app.route('/home/register/')
def Register():
	return render_template('register.html')
	
if  __name__=='__main__':
	app.run(debug=True)
