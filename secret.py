import jwt
import datetime

ADMIN_KEY = "apipassword"
exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=120)
privatekey = "privatejwtkey"
publickey = "publicrestkey"
emailpass = "emailpass"


def getToken(id, name, useremail):
    token = jwt.encode({'id': id, 'name': name, 'useremail': useremail, 'exp': exp},
                       privatekey, algorithm="HS256")
    return token


def decodeToken(encoded):
    try:
        token = jwt.decode(encoded, privatekey, algorithms=["HS256"])
        print(token)
        return token, False
    except:
        return None, True
