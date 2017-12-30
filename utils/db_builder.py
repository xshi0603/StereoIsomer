import sqlite3
import csv
import hashlib
import uuid

#still need to implement generators stuff

#==========================================================
'''
TABLE CREATION
Database info.db
Tables: credentials
'''

def tableCreation():
    f = "data/info.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    user_table = 'CREATE TABLE credentials (id INTEGER, username TEXT, password BLOB);'
    c.execute(user_table)
    stats_table = 'CREATE TABLE stats (id INTEGER, cookies INTEGER, cps INTEGER, generators BLOB);'
    c.execute(stats_table)
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
    userCount = c.execute('SELECT COUNT(*) FROM credentials;')
    new_userID = 0
    for x in userCount:
        new_userID = x[0]
    hash_pass = hash_password(new_password)
    c.execute('INSERT INTO credentials VALUES (?,?,?)',[new_userID, new_username, hash_pass])
    c.execute('INSERT INTO stats VALUES (?,?,?,?)',[new_userID, 0, 0, 0])
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

#accessor to get password based on username
def getPass(username):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = "SELECT username, password FROM credentials;"
    info = c.execute(command)
    retVal = None
    for entry in info:
        if str(entry[0]) == username:
            retVal = str(entry[1])
    db.close()
    return retVal


def getUserID(username):
    f = "data/info.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    command = "SELECT username, id FROM credentials"
    info = c.execute(command)
    retVal = None
    for user in info:
        if str(user[0]) == username:
            retVal = str(user[1])
    db.close()
    return retVal

def getCookies(username):
    f = "data/info.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    user_id = getUserID(username)
    cookies = c.execute('SELECT cookies FROM stats WHERE id= "' + user_id + '";')
    retVal = (cookies.fetchone())[0]
    db.close()
    return retVal

def getCPS(username):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(username)
    cps_val = c.execute('SELECT cps FROM stats WHERE id = ' + str(user_id) + ';')
    retVal = (cps_val.fetchone())[0]
    db.close()
    return retVal


#================================================================

#MUTATORS

def addCookies(user, c_count):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    stuff = c.execute('SELECT cookies FROM stats WHERE id= ' + user_id + ';')
    old_content = stuff.fetchone()
    #print 'OLD_CONTENT...'
    #print old_content
    cookies = old_content[0] + c_count
    c.execute("UPDATE stats SET cookies =" + str(cookies) + " WHERE id = " + user_id)
    db.commit()
    db.close()

def setCPS(user, new_cps):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    cps = str(new_cps)
    c.execute("UPDATE stats SET cps = " + cps + " WHERE id = " + user_id)
    db.commit()
    db.close()

#TESTING

if __name__ == '__main__':
    #create table
    tableCreation()

    #add users
    addUser('manahal','tabassum')
    addUser('bob', '123')

    print getUserID('manahal')
    print getUserID('bob')

    #check getPass
    print 'manahal pass:'
    print getPass('manahal')
    print 'bob pass:'
    print getPass('bob')

    #check authenticate
    authenticate('manahal','tabassum')
    authenticate('joe','123')
    authenticate('bob','sdilblf')

    print 'original cookie count manahal'
    print getCookies('manahal')
    addCookies('manahal', 100)
    print 'new cookie count manahal'
    print getCookies('manahal')

    print 'original cps manahal'
    print getCPS('manahal')
    setCPS('manahal', 50)
    print 'new cps manahal'
    print getCPS('manahal')
