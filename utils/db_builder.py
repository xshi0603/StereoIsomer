import sqlite3
import csv
import hashlib
import uuid


#==========================================================
'''
TABLE CREATION
Database info.db
Tables: users, stories, updates
'''

def tableCreation():
    f = "data/info.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    user_table = 'CREATE TABLE users (username TEXT, password BLOB);'
    c.execute(user_table)
    db.commit()
    db.close()

#==========================================================

#ADD VALUES TO TABLES

def hash_password(password):
    key = uuid.uuid4().hex
    return hashlib.sha256(key.encode() + password.encode()).hexdigest()+':' + key

#add a user
def addUser(new_username, new_password):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    hash_pass = hash_password(new_password)
    c.execute('INSERT INTO users VALUES (?,?)',[new_username, hash_pass])
    db.commit()
    db.close()

#============================================================

#USER AUTHENTICATION
def checkPassword(hashed_password, user_password):
    password, key = hashed_password.split(':')
    return password == hashlib.sha256(key.encode()+user_password.encode()).hexdigest()

def authenticate(user, passw):
    info = getPass(user)
    if info == None:
        print 'user does not exist'
        return 0 #user doesn't exist
    elif checkPassword(info, passw):
        print 'logged in'
        return 1 #user and password correct
    else:
        print 'incorrect password'
        return -2 #password incorrect

#==============================================================

#ACCESSORS

def getPass(username):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = "SELECT username, password FROM users"
    info = c.execute(command)
    retVal = None
    for entry in info:
        if str(entry[0]) == username:
            retVal = str(entry[1])
    db.close()
    return retVal

#================================================================

#TESTING

if __name__ == '__main__':
    #create table
    tableCreation()

    #add users
    addUser('manahal','tabassum')
    addUser('bob', '123')

    #check getPass
    print getPass('manahal')
    print getPass('joe')

    #check authenticate
    authenticate('manahal','tabassum')
    authenticate('joe','123')
    authenticate('bob','sdilblf')
