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