from firebase import Firebase
import os
if os.getenv('PRODUCTION')!="yes":
    import dotenv
    dotenv.find_dotenv()
configfb = {
    "apiKey": os.getenv('firebase_key'),
    "authDomain": "142115676780.firebaseapp.com",
    "databaseURL": "https://chatik-dcd54.firebaseio.com/",
    "storageBucket": "chatik-dcd54.appspot.com"
}
firebase = Firebase(configfb)
db = firebase.database()

def test():
    print(db.child("prefix").get().val())