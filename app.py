from flask import Flask, render_template, request, session, redirect, url_for, flash
import os, csv, sqlite3, hashlib, uuid, requests
#from datetime import datetime
#from utils import api_library, dbLibrary
#import json

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
    dbTunes = dbLibrary.openDb("data/tunes.db")
    cursor = dbLibrary.createCursor(dbTunes)
    input_username = request.form['username']
    input_password = request.form['password']

    if input_username=='' or input_password=='' :
        flash("Please Fill In All Fields")
        return redirect(url_for('login'))

    if "'" in input_username or "'" in input_password:
        flash("Invalid Login Info")
        return redirect(url_for('login'))

    hashed_passCursor = cursor.execute("SELECT password FROM users WHERE username = '" + input_username + "'")
    numPasses = 0 #should end up being 1 if all fields were filled

    for item in hashed_passCursor:
        numPasses += 1
        hashed_pass = item[0]
        print item[0]

    dbLibrary.closeFile(dbTunes)

    if  numPasses == 0:
        flash ("User doesn't exist")
        return redirect(url_for('login'))

    elif check_password(hashed_pass, input_password):
        flash("Login Successful")
        session["username"] = input_username;#in order to keep track of user
        return redirect(url_for('diary'))

    else:
        flash("Invalid Login Information")
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
    dbTunes = dbLibrary.openDb("data/tunes.db")
    cursor = dbLibrary.createCursor(dbTunes)
    #print request.form
    username = request.form['newUsername']
    password = request.form['newPassword']

    if username == '' or password == '':
        dbLibrary.closeFile(dbTunes)
        flash("Please Fill In All Fields")
        return redirect(url_for('account'))

    elif len(password)< 6:
        dbLibrary.closeFile(dbTunes)
        flash("Password must have at least 6 characters")
        return redirect(url_for('account'))

    elif (' ' in username or ' ' in password or "'" in username or "'" in password or '"' in username or '"' in password ):
        dbLibrary.closeFile(dbTunes)
        flash("Username and Password cannot contain the space,single quote, or double quote character")
        return redirect(url_for('account'))

    password = hash_password(password)
    sameUser = cursor.execute("SELECT username FROM users WHERE username = '" + username +"'")

    counter = 0 #should remain 0 if valid username since username needs to be unique
    for item in sameUser:
        counter += 1

    if counter == 0:
        dbLibrary.insertRow('users',['username', 'password', 'sadness', 'joy', 'anger', 'fear'],[username, password, "base", "base", "base", "base"],cursor)
        flash("Account Successfully Created")
        dbLibrary.commit(dbTunes)
        dbLibrary.closeFile(dbTunes)
        return redirect(url_for('login'))

    else:
        flash("Invalid: Username taken")
        dbLibrary.commit(dbTunes)
        dbLibrary.closeFile(dbTunes)
        return redirect(url_for('account'))

#-----------------------------------------------------------

#---------------------GAME-------------------------------

@cookie_app.route('/game', methods=['GET'])
def game():
    #if 'username' not in session:
    #    flash("Session timed out")
    #    return redirect(url_for('login'))
    #current_user = session["username"]

    return render_template("game.html")

#--------------------------------------------------------

#---------------------LOGGING OUT------------------------

@cookie_app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        flash("Logged out.")
    return redirect(url_for("root"))

#--------------------------------------------------------

#---------------------WEATHER----------------------------

def getWeather():
    key = open('wunderground_api_key.txt', 'rb').read()
    #print key
    #data = newJSON
    #response = requests.get('http://api.wunderground.com/api/ab6209433554e030/conditions/q/NY/New_York_City.json')   
    url = 'http://api.wunderground.com/api/' + key + '/conditions/q/CA/San_Francisco.json'                                                            
    #print(url)
    response = requests.get(url)
    response = response.json()
    temperature = response['current_observation']['temp_f']
    #print temperature
    return temperature

@cookie_app.route('/weather', methods=['GET'])
def weather():
    print getWeather()
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
    #not logged in
    flash("Please log in first")
    return redirect(url_for("root"))

#--------------------------------------------------------

if __name__ == '__main__':
    cookie_app.debug = True
    cookie_app.run()
