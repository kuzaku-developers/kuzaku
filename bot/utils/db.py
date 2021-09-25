from firebase import Firebase
import os
if os.getenv('PRODUCTION')!="yes":
    import dotenv
    dotenv.find_dotenv()
configfb = {
    "apiKey": os.getenv('fapiKey'),
    "authDomain": os.getenv('fauthDomain'),
    "databaseURL": os.getenv('fdatabaseURL'),
    "storageBucket": os.getenv('fstorageBucket')
}
firebase = Firebase(configfb)
db = firebase.database()

def getdb():
    return dict(db.child("db").get().val())

def setdb(dbb):
    db.child("db").set(dbb)

def geteco(guildid, id):
    return dict(db.child('db').child("eco").child(guildid).child(id).get().val())

def seteco(guildid, id, xp, lvl, nextxp):
    data={'xp':xp, 'lvl': lvl, 'nextxp': nextxp}
    db.child("db").child('eco').child(guildid).child(id).set(data)
def addpromo(promocode, uses):
    data={'promocode': promocode, 'uses': uses}
    db.child("db").child('promocodes').push(data)
def getpromos():
    return dict(getdb()['promocodes'])
def addusepromo(promocodeid, uses):
    data={'usedby':uses}
    try:
        db.child("db").child('promocodes').child(promocodeid).update(data)
    except Exception as e:
        print(e)
def setpromouses(promocodeid, uses):
    data={'uses': uses}
    try:
        db.child("db").child('promocodes').child(promocodeid).update(data)
    except Exception as e:
        print(e)
def minusoneguild(userid):
    data=dict(getdb()['premium'])[str(userid)]
    data['count'] = str(int(data['count'])-1)
    db.child("db").child('premium').child(str(userid)).set(data)
def setsupporter(guildid, status):
    if status:
        data={'premium' : 'True'}
        db.child("db").child('premium').child('guilds').child(guildid).set(data)
def getpremium(guildid):
    for i in dict(getdb()['premium'])['guilds']:
        if str(i) == str(guildid):
            return True
    return False
def dbgetrpid(id_user):
    all_users=db.child("rp").get().val()
    rpid=len(all_users)+1
    return rpid
def dbrpaddmoney(id_user, money):
    data=dbrpgetuser(id_user)
    try:
        data['rubles']=int(data['rubles'])+int(money)
    except:
        data['rubles'] = str(int(0) + int(money))
    db.child("rp").child(id_user).set(data)

def dbrpadddollars(id_user, money):
    data=dbrpgetuser(id_user)
    try:
        data['dollars']=int(data['dollars'])+int(money)
    except:
        data['dollars'] = str(int(0) + int(money))
    db.child("rp").child(id_user).set(data)

def dbrpsethome(id_user, home):
    data=dbrpgetuser(id_user)
    data['home']=home
    db.child("rp").child(id_user).set(data)

def dbrpsetjson(id_user, name, value):
    data=dbrpgetuser(id_user)
    data[name]=value
    db.child("rp").child(id_user).set(data)

def dbrpsetcar(id_user, car):
    data=dbrpgetuser(id_user)
    data['car']=car
    db.child("rp").child(id_user).set(data)
def dbrpsetresume(id_user, resume):
    data=dbrpgetuser(id_user)
    data['resume']=resume
    db.child("rp").child(id_user).set(data)

def dbsetrp(id_user, rpname, naviki):
    data = {'idrp': dbgetrpid(id_user), 'rpname': rpname, "naviki": naviki, 'money': 0, 'home': False}
    db.child("rp").child(id_user).set(data)
def dbrpgetuser(id_user):
    all_users=db.child("rp").get()
    for user in all_users.each():  # все элементы
        kkey = user.key()  # ключ

        if str(kkey) == str(id_user):  # проверка на равенство
            a = user.val()  # true(1) или false(0) (в бд так)
            try:
                return a# .
            except:
                return {}


def dbrpgetcolumn(column):
    all_users = db.child(column).get().val().items()
    try:
        return dict(all_users)  # .
    except:
        return {}
