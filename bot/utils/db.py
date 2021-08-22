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
def minusoneguild(userid):
    data=dict(getdb()['premium'])[str(userid)]
    data['count'] = str(int(data['count'])-1)
    db.child("db").child('premium').child(str(userid)).set(data)
def setsupporter(guildid, status):
    if status:
        data={'premium' : 'True'}
        db.child("db").child('premium').child('guilds').child(guildid).set(data)
def getpremium(guildid):
    print(dict(getdb()['premium'])['guilds'])
    for i in dict(getdb()['premium'])['guilds']:
        print(i)
        if str(i) == str(guildid):
            return True
    return False