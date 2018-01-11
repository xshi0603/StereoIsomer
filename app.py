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
    
    db_builder.addUser(username, password)
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
    #if 'username' not in session:
    #    flash("Session timed out")
    #    return redirect(url_for('login'))
    #current_user = session["username"]


    #return render_template("game.html", temp = getWeather())
    return render_template("game.html")

#--------------------------------------------------------

#---------------------SAVE-------------------------------

@cookie_app.route('/save', methods=['GET', 'POST'])
def save():
    #data = request.args.get("text")
    username = request.form["username"]
    cookies = request.form["cookies"]
    gen0 = request.form["gen0"]
    gen1 = request.form["gen1"]
    print "username is:"
    print username
    print "cookies is:"
    print cookies
    print "gen0 is:"
    print gen0
    print "gen1 is:"
    print gen1
    #response = {'uc' : data }
    #print "after dumping: \n"
    #response = json.dumps(response)
    #print response
    flash("haelo")
    return username

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

#---------------------MISC-------------------------------

@cookie_app.route('/credits', methods=['GET'])
def credits():
    return render_template("credits.html")

@cookie_app.route('/leaderboard', methods=['GET'])
def leaderboard():
    return render_template("leaderboard.html")

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
