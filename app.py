from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from utils import  db_builder
import os, csv, sqlite3, hashlib, uuid, requests, json


#----------------------ENCRYPTION---------------------------

def hash_password(password):
    key = uuid.uuid4().hex
    return hashlib.sha256(key.encode() + password.encode()).hexdigest() + ':' + key

def check_password(hashed_password, user_password):
    password,key = hashed_password.split(":")
    return password == hashlib.sha256(key.encode() + user_password.encode()).hexdigest()

#-------------------------------------------------------------------

cookie_app = Flask(__name__)
cookie_app.secret_key = os.urandom(32)

user = ""

#----------------------HOME PAGE-------------------------------

@cookie_app.route("/")
def root():
    return render_template("home.html")

#-------------------------------------------------------------------

#------------------------LOGIN----------------------------------

@cookie_app.route("/login", methods = ['POST' , 'GET'])
def login():
    if 'username' in session:
        return redirect(url_for('game'))
    return render_template("login.html")

@cookie_app.route("/authenticate",methods = ['POST','GET']) #old stuff
def authenticate():
    input_username = request.form['username']
    input_password = request.form['password']

    status = db_builder.authenticate(input_username, input_password)

    if (status == 0):
        flash("user dne")
        return redirect(url_for('login')) #user dne
    elif (status == 1): #sucessful
        session['user'] = input_username
        return redirect(url_for('game'))
    
    flash("password wrong")
    return redirect(url_for('login'))
    
#-------------------------------------------------------------------

#---------------CREATING AN ACCOUNT----------------------------------

@cookie_app.route("/account", methods = ['POST' , 'GET'])
def account():
    if 'username' in session:
        return redirect(url_for('game'))
    return render_template("register.html")

@cookie_app.route("/accountSubmit", methods = ['POST' , 'GET'])
def accountSubmit():
    username = request.form['newUsername']
    password = request.form['newPassword']
    
    status = db_builder.addUser(username, password)
    print status
    if (status == False):
        flash("User already exists")
    return redirect(url_for('login'))
    
#-----------------------------------------------------------

#---------------------WEATHER----------------------------

def getWeather():
    key = open('wunderground_api_key.txt', 'rb').read() 
    url = 'http://api.wunderground.com/api/' + key + '/conditions/q/CA/San_Francisco.json'                         
    response = requests.get(url)
    response = response.json()
    temperature = response['current_observation']['temp_f']
    return temperature

@cookie_app.route('/weather', methods=['GET'])
def weather():
    print getWeather()
    return redirect(url_for("root"))

#--------------------------------------------------------

#---------------------GAME-------------------------------

@cookie_app.route('/game', methods=['GET'])
def game():
    if 'user' not in session:
        flash("Session timed out. Please log in")
        return redirect(url_for('login'))

    return render_template("game.html", temp = getWeather())
    #return render_template("game.html")

#--------------------------------------------------------

#---------------------SAVE-------------------------------


@cookie_app.route('/save', methods=['GET', 'POST'])
def save():
    #data = request.args.get("text")              
    username = request.form["username"]
    cookies = request.form["cookies"]
    gen0 = request.form["gen0"]
    gen1 = request.form["gen1"]
    gen2 = request.form["gen2"]
    clickNum = request.form["clickNum"]
    gen0Up = request.form["gen0Up"]
    gen1Up = request.form["gen1Up"]
    gen2Up = request.form["gen2Up"]
    db_builder.setCookies(username, cookies)
    db_builder.setGen1(username, gen0)
    db_builder.setGen2(username, gen1)
    db_builder.setGen3(username, gen2)
    db_builder.setCPS(username, clickNum)
    db_builder.setUpgrade1(username, gen0Up)
    db_builder.setUpgrade2(username, gen1Up)
    db_builder.setUpgrade3(username, gen2Up)
    return "filler";


@cookie_app.route('/getpythonuser')
def get_python_user():
    if 'user' in session:
        username = session['user']
        return json.dumps(session['user'])
    return json.dumps("no one is logged in yet")


@cookie_app.route('/getpythoncookies')
def get_python_cookies():
    if 'user' in session:
        username = session['user']
        cookies = db_builder.getCookies(username)
        return json.dumps(cookies)
    return json.dumps("no one is logged in yet")

@cookie_app.route('/getpythongen0')
def get_python_gen0():
    if 'user' in session:
        username = session['user']
        gen0 = db_builder.getGen1(username)
        return json.dumps(gen0)
    return json.dumps("no one is logged in yet")

@cookie_app.route('/getpythongen1')
def get_python_gen1():
    if 'user' in session:
        username = session['user']
        gen1 = db_builder.getGen2(username)
        return json.dumps(gen1)
    return json.dumps("no one is logged in yet")

@cookie_app.route('/getpythongen2')
def get_python_gen2():
    if 'user' in session:
        username = session['user']
        gen2 = db_builder.getGen3(username)
        return json.dumps(gen2)
    return json.dumps("no one is logged in yet")

@cookie_app.route('/getpythonclick')
def get_python_click():
    if 'user' in session:
        username = session['user']
        click = db_builder.getCPS(username)
        return json.dumps(click)
    return json.dumps("no one is logged in yet")

@cookie_app.route('/getpythonup0')
def get_python_up0():
    if 'user' in session:
        username = session['user']
        up0 = db_builder.getUpgrade1(username)
        return json.dumps(up0)
    return json.dumps("no one is logged in yet")

@cookie_app.route('/getpythonup1')
def get_python_up1():
    if 'user' in session:
        username = session['user']
        up1 = db_builder.getUpgrade2(username)
        return json.dumps(up1)
    return json.dumps("no one is logged in yet")

@cookie_app.route('/getpythonup2')
def get_python_up2():
    if 'user' in session:
        username = session['user']
        up2 = db_builder.getUpgrade3(username)
        return json.dumps(up2)
    return json.dumps("no one is logged in yet")


'''    
    return render_templater("game.html", temp = getWeather())

@app.route("/")
    def index():
        return render_template("index.html")
    
@app.route("/foo")
def upcase():
    data = request.args.get("text")
    print data
    response = {'uc' : data.upper() }
    return json.dumps(response)
'''


#--------------------------------------------------------

#---------------------LOGGING OUT------------------------

@cookie_app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        flash("Logged out.")
    return redirect(url_for("root"))

#--------------------------------------------------------

#------------------LEADERBOARD---------------------------

@cookie_app.route('/leaderboard', methods=['GET'])
def leaderboard():
    list = db_builder.leaderboard()
    return render_template("leaderboard.html", lb = list)

#--------------------------------------------------------

#---------------------MISC-------------------------------

@cookie_app.route('/credits', methods=['GET'])
def credits():
    return render_template("credits.html")

@cookie_app.route('/achievements', methods=['GET'])
def achievements():
    if 'username' in session:
        return render_template("achievements.html")
    flash("Please log in first")
    return redirect(url_for("root"))

#--------------------------------------------------------

if __name__ == '__main__':
    cookie_app.debug = True
    cookie_app.run()
