from firebase import Firebase
import os

if os.getenv("PRODUCTION") != "yes":
    import dotenv

    dotenv.find_dotenv()
configfb = {
    "apiKey": os.getenv("fapiKey"),
    "authDomain": os.getenv("fauthDomain"),
    "databaseURL": os.getenv("fdatabaseURL"),
    "storageBucket": os.getenv("fstorageBucket"),
}
firebase = Firebase(configfb)
db = firebase.database()


def getdb():
    return dict(db.child("db").get().val())


def setdb(dbb):
    db.child("db").set(dbb)


def geteco(guildid, id):
    return dict(db.child("db").child("eco").child(guildid).child(id).get().val())


def seteco(guildid, id, xp, lvl, nextxp):
    data = {"xp": xp, "lvl": lvl, "nextxp": nextxp}
    db.child("db").child("eco").child(guildid).child(id).set(data)


def addpromo(promocode, uses):
    data = {"promocode": promocode, "uses": uses}
    db.child("db").child("promocodes").push(data)


def getpromos():
    return dict(getdb()["promocodes"])

def dbgetlistt(id_user):
    global a
    a=False
    try:
        all_users = db.child("blacklist").get()
        for user in all_users.each():
            kkey = user.key()
            print(f'kkey: {kkey}')
            print(f'id:{id_user}')
            if str(kkey) == str(id_user):
                a = True
                print(f'True')
                return a
            else:
                a=False
    except:
        return False

def dbgetlist(id_user): #получение
    all_users = db.child("blacklist").get() #получение всей таблицы
    if dbgetlistt(id_user): #если есть элемент
        for user in all_users.each(): #все элементы
            kkey = user.key() #ключ

            if str(kkey) == str(id_user): #проверка на равенство
                a = user.val() #true(1) или false(0) (в бд так)
                print('1') #дебаг и все
                return a["blacklist"] #.
    else:
        print('dfghjgkh') #дебаг
        return 0 #возврат 0 (false)

def dbsetlist(id_user, orka):
    if orka==1:
        data = {'blacklist': orka}
        db.child("blacklist").child(id_user).set(data)
    elif orka==0:
        data = {'blacklist': orka}
        db.child("blacklist").child(id_user).set(data)
    
def addusepromo(promocodeid, uses):
    data = {"usedby": uses}
    try:
        db.child("db").child("promocodes").child(promocodeid).update(data)
    except Exception as e:
        print(e)


def setpromouses(promocodeid, uses):
    data = {"uses": uses}
    try:
        db.child("db").child("promocodes").child(promocodeid).update(data)
    except Exception as e:
        print(e)


def usedcmd():
    data = dict(getdb()["cmds"])
    data["count"] = str(int(data["count"]) + 1)
    db.child("db").child("cmds").set(data)


def usedcommands():
    data = dict(getdb()["cmds"])
    return data["count"]


def minusoneguild(userid):
    data = dict(getdb()["premium"])[str(userid)]
    data["count"] = str(int(data["count"]) - 1)
    db.child("db").child("premium").child(str(userid)).set(data)


def setsupporter(guildid, status):
    if status:
        data = {"premium": "True"}
        db.child("db").child("premium").child("guilds").child(guildid).set(data)


def change_config(guild_id, key, value):
    data = {key: value}
    try:
        db.child("db").child("settings").child(guild_id).update(data)
        return True
    except:
        return False


def get_config(guild_id):
    if db.child("db").child("settings").child(guild_id).get().val():
        return db.child("db").child("settings").child(guild_id).get().val()
    else:
        change_config(guild_id, "eco_enabled", "true")
        change_config(guild_id, "xppermsg", "1")
        return {"eco_enabled": "true", "xppermsg": "1"}


def setpremium(userid, status, count):
    data = {"premium": str(status), "count": count}
    db.child("db").child("premium").child(userid).set(data)
    print(status)


def getpremium(guildid):
    for i in dict(getdb()["premium"])["guilds"]:
        if str(i) == str(guildid):
            return True
    return False


def dbgetrpid(id_user):
    all_users = db.child("rp").child("users").get().val()
    rpid = len(all_users)
    print(len(all_users))
    return rpid


def dbrpaddmoney(id_user, money):
    if id_user == "federation":
        data = dict(dbrpgetdef(id_user))
        print(data)
        data["rubles"] = int(data["rubles"]) + int(money)
        db.child("rp").child(id_user).set(data)
    else:
        data = dict(dbrpgetuser(id_user))
        print(data)
        data["rubles"] = int(data["rubles"]) + int(money)
        db.child("rp").child("users").child(id_user).set(data)


def dbrpadddollars(id_user, money):
    if id_user == "federation":
        data = dict(dbrpgetdef(id_user))
        print(data)
        data["dollars"] = int(data["dollars"]) + int(money)
        db.child("rp").child(id_user).set(data)
    else:
        data = dict(dbrpgetuser(id_user))
        print(data)
        data["dollars"] = int(data["dollars"]) + int(money)
        db.child("rp").child("users").child(id_user).set(data)


def dbrpadddollars(id_user, money):
    data = dbrpgetuser(id_user)
    try:
        data["dollars"] = int(data["dollars"]) + int(money)
    except:
        data["dollars"] = str(int(0) + int(money))
    db.child("rp").child("users").child(id_user).set(data)


def dbrpsethome(id_user, home):
    data = dbrpgetuser(id_user)
    data["home"] = home
    db.child("rp").child("users").child(id_user).set(data)


def dbrpsetjson(id_user, name, value):
    data = dbrpgetuser(id_user)
    data[name] = value
    db.child("rp").child("users").child(id_user).set(data)


def dbrpsetcar(id_user, car):
    data = dbrpgetuser(id_user)
    data["car"] = car
    db.child("rp").child("users").child(id_user).set(data)


def dbrpsetresume(id_user, resume):
    data = dbrpgetuser(id_user)
    data["resume"] = resume
    db.child("rp").child("users").child(id_user).set(data)


def dbsetrp(id_user, rpname, naviki):
    data = {
        "idrp": dbgetrpid(id_user),
        "rpname": rpname,
        "naviki": naviki,
        "money": 0,
        "home": False,
        "rubles": 0,
    }
    db.child("rp").child("users").child(id_user).set(data)


def dbrpgetdef(id_user):
    all_users = db.child("rp").get()
    for user in all_users.each():  # все элементы
        kkey = user.key()  # ключ

        if str(kkey) == str(id_user):  # проверка на равенство
            a = user.val()  # true(1) или false(0) (в бд так)
            try:
                return a  # .
            except:
                return {}


def dbrpgetuser(id_user):
    all_users = db.child("rp").child("users").get()
    for user in all_users.each():  # все элементы
        kkey = user.key()  # ключ

        if str(kkey) == str(id_user):  # проверка на равенство
            a = user.val()
            print(a)  # true(1) или false(0) (в бд так)
            try:
                return dict(a)  # .
            except:
                return {}


def dbrpgetcolumn(column):
    all_users = db.child(column).get().val().items()
    try:
        return dict(all_users)  # .
    except:
        return {}
