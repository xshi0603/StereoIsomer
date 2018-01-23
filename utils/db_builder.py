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
    achievements_table = 'CREATE TABLE achievements (id INTEGER, achievement TEXT)'
    c.execute(achievements_table)
    upgrades_table = 'CREATE TABLE upgrades (id INTEGER, upgrade1 INTEGER, upgrade2 INTEGER, upgrade3 INTEGER)'
    c.execute(upgrades_table)
    generators_table = 'CREATE TABLE generators (id INTEGER, generator1 INTEGER, generator2 INTEGER, generator3 INTEGER);'
    c.execute(generators_table)
    stats_table = 'CREATE TABLE stats (id INTEGER, cookies INTEGER, cps INTEGER);'
    c.execute(stats_table)
    db.commit()
    db.close()

#==========================================================

#ADD VALUES TO TABLES

def hash_password(password):
    key = uuid.uuid4().hex
    return hashlib.sha256(key.encode() + password.encode()).hexdigest()+':' + key

def checkUsername(user):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    usernames = c.execute('SELECT username FROM credentials;')
    for x in usernames:
        print x[0]
        if (x[0] == user):
            return False
        else:
            return True

#add a user
def addUser(new_username, new_password):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    if (checkUsername(new_username) == False):
        print 'username already used'
        return False
    userCount = c.execute('SELECT COUNT(*) FROM credentials;')
    new_userID = 0
    for x in userCount:
        new_userID = x[0]
    hash_pass = hash_password(new_password)
    c.execute('INSERT INTO credentials VALUES (?,?,?)',[new_userID, new_username, hash_pass])
    c.execute('INSERT INTO achievements VALUES (?,?)',[new_userID, ''])
    c.execute('INSERT INTO upgrades VALUES (?,?,?,?)',[new_userID, 0, 0, 0])
    c.execute('INSERT INTO generators VALUES (?,?,?,?)',[new_userID, 0, 0, 0])
    c.execute('INSERT INTO stats VALUES (?,?,?)',[new_userID, 0, 0])
    db.commit()
    db.close()
    return True

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

def getUsername(uID):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = "SELECT username FROM credentials WHERE id = " + str(uID) + ";"
    info = c.execute(command)
    retVal = c.fetchall()[0][0]
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

def getAchievements(user):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    achs = ((c.execute('SELECT achievement FROM achievements WHERE id = ' + str(user_id) + ';')).fetchall())[0][0]
    stuff = achs[0:len(achs)-1]
    #print stuff
    ach_list = (stuff.split(';'))
    #print "Final list.."
    #print ach_list
    db.close()
    return ach_list
'''
def getUpgrades(user):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    upgrades = ((c.execute('SELECT upgrade FROM upgrades WHERE id = ' + str(user_id) + ';')).fetchall())[0][0]
    stuff = upgrades[0:len(upgrades)-1]
    #print stuff
    up_list = (stuff.split(';'))
    #print "Final list.."
    #print up_list
    db.close()
    return up_list
'''

def getGen1(user):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    gen_num = ((c.execute('SELECT generator1 FROM generators WHERE id = ' + str(user_id) + ';')).fetchall())[0][0]
    db.close()
    return gen_num

def getGen2(user):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    gen_num = ((c.execute('SELECT generator2 FROM generators WHERE id = ' + str(user_id) + ';')).fetchall())[0][0]
    db.close()
    return gen_num

def getGen3(user):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    gen_num = ((c.execute('SELECT generator3 FROM generators WHERE id = ' + str(user_id) + ';')).fetchall())[0][0]
    db.close()
    return gen_num

def getUpgrade1(user):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    upgrade_num = ((c.execute('SELECT upgrade1 FROM upgrades WHERE id = ' + str(user_id) + ';')).fetchall())[0][0]
    db.close()
    return upgrade_num

def getUpgrade2(user):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    upgrade_num = ((c.execute('SELECT upgrade2 FROM upgrades WHERE id = ' + str(user_id) + ';')).fetchall())[0][0]
    db.close()
    return upgrade_num

def getUpgrade3(user):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    upgrade_num = ((c.execute('SELECT upgrade3 FROM upgrades WHERE id = ' + str(user_id) + ';')).fetchall())[0][0]
    db.close()
    return upgrade_num

'''
def getGenerators(user):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    gens = ((c.execute('SELECT generators FROM stats WHERE id = ' + str(user_id) + ';')).fetchall())[0][0]
    stuff = gens[0:len(gens)-1]
    #print stuff
    gen_list = (stuff.split(';'))
    #print "Final list.."
    #print gen_list
    return gen_list
'''
    

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

def setCookies(user, c_count):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    cookies = str(c_count)
    c.execute("UPDATE stats SET cookies = " + cookies + " WHERE id = " + user_id)
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

def setGen1(user, num):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    gen_num = str(num)
    c.execute("UPDATE generators SET generator1 = " + gen_num + " WHERE id = " + user_id)
    db.commit()
    db.close()

def setGen2(user, num):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    gen_num = str(num)
    c.execute("UPDATE generators SET generator2 = " + gen_num + " WHERE id = " + user_id)
    db.commit()
    db.close()

def setGen3(user, num):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    gen_num = str(num)
    c.execute("UPDATE generators SET generator3 = " + gen_num + " WHERE id = " + user_id)
    db.commit()
    db.close()

def setUpgrade1(user, num):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    upgrade_num = str(num)
    c.execute("UPDATE upgrades SET upgrade1 = " + upgrade_num + " WHERE id = " + user_id)
    db.commit()
    db.close()

def setUpgrade2(user, num):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    upgrade_num = str(num)
    c.execute("UPDATE upgrades SET upgrade2 = " + upgrade_num + " WHERE id = " + user_id)
    db.commit()
    db.close()

def setUpgrade3(user, num):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    upgrade_num = str(num)
    c.execute("UPDATE upgrades SET upgrade3 = " + upgrade_num + " WHERE id = " + user_id)
    db.commit()
    db.close()

#=========================================================================
#Adding achievements, upgrades, generators
def addAchievement(user, ach):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    stuff = c.execute('SELECT achievement FROM achievements WHERE id= ' + user_id + ';')
    old_content = stuff.fetchone()
    print 'OLD_CONTENT...'
    print old_content
    new_content = old_content[0] + ach + ";"
    print 'NEW_CONTENT...'
    print new_content
    c.execute("UPDATE achievements SET achievement = '" + new_content + "' WHERE id = " + user_id + ";")
    #c.execute(command)
    db.commit()
    db.close()
'''
def addUpgrade(user, new_upgrade):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    stuff = c.execute('SELECT upgrade FROM upgrades WHERE id= ' + user_id + ';')
    old_content = stuff.fetchone()
    #print 'OLD_CONTENT...'
    #print old_content
    new_content = old_content[0] + new_upgrade + ';'
    c.execute("UPDATE upgrades SET upgrade = '" + new_content + "' WHERE id = " + user_id)
    db.commit()
    db.close()
'''
'''
def addGenerator(user, new_gen):
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    user_id = getUserID(user)
    stuff = c.execute('SELECT generators FROM stats WHERE id= ' + user_id + ';')
    old_content = stuff.fetchone()
    #print 'OLD_CONTENT...'
    #print old_content
    new_content = old_content[0] + new_gen + ';'
    c.execute("UPDATE stats SET generators = '" + new_content + "' WHERE id = " + user_id)
    db.commit()
    db.close()
'''

#=========================================================================
'''
returns a dictionary in which key value is username and key value is list
list is as follows: [(u'hamlet', [3, 1000]), (u'bob', [1, 700]), (u'manahal', [0, 500]), (u'joe', [2, 0])]

'''

def leaderboard():
    f="data/info.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    info = c.execute('SELECT * FROM stats;')
    d = {}
    for x in info:
        #print x[0]
        #print x[1]
        username = getUsername(x[0])
        cookies = getCookies(username)
        d[username] = [x[0], cookies]
    
    sort = sorted(d.iteritems(), key=lambda value:value[1][1])
    print "sorted something"
    print sort
    #print "unsorted dict"
    #print d
    d_sort = []
    for x in sort:
        print "entry..."
        print x
        print "name"
        print x[0]
        print "id"
        print x[1][0]
        print "cookie count"
        print x[1][1]
        d_sort.insert(0,x)
    return d_sort
    db.commit()
    db.close()

    
#TESTING

if __name__ == '__main__':
    #create table
    tableCreation()

    #add users
    addUser('manahal','tabassum')
    addUser('bob', '123')
    addUser('joe', '123')
    addUser('hamlet','123')

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
    setCookies('manahal', 500)
    setCookies('bob', 700)
    setCookies('hamlet', 1000)
    print getCookies('manahal')

    print 'original cps manahal'
    print getCPS('manahal')
    setCPS('manahal', 50)
    print 'new cps manahal'
    print getCPS('manahal')

    addAchievement('manahal','ach1')
    addAchievement('manahal','ach2')
    addAchievement('manahal','ach3')
    addAchievement('manahal','ach4')

    #addUpgrade('manahal','upgrade1')
    #addUpgrade('manahal','upgrade2')
    #addUpgrade('manahal','upgrade3')
    #addUpgrade('manahal','upgrade4')

    #addGenerator('manahal','gen1')
    #addGenerator('manahal','gen2')
    #addGenerator('manahal','gen3')
    #addGenerator('manahal','gen4')

    print getAchievements('manahal')
    #print getUpgrades('manahal')
    #print getGenerators('manahal')

    #checkUsername('manahal')
    addUser('manahal','hvkdjfg')
    print getUsername(0)
    print getUsername(1)
    #leaderboard()

    setUpgrade1('manahal', 5)
    setUpgrade2('manahal', 10)
    setUpgrade3('manahal', 15)

    print "upgrade1"
    print getUpgrade1('manahal')
    print "upgrade2"
    print getUpgrade2('manahal')
    print "upgrade3"
    print getUpgrade3('manahal')

    print getGen1('manahal')
    setGen1('manahal', 10)
    print getGen1('manahal')

    print leaderboard()
