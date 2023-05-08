import jwt
import datetime
from base64 import b64decode

ADMIN_KEY = "apipassword"
exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
privatekey = "privatejwtkey"
publickey = "publicrestkey"
emailpass = "iaeu swuj ovop raxu"


def getToken(id, name, useremail):
    token = jwt.encode({'id': id, 'name': name, 'useremail': useremail, 'exp': exp},
                       privatekey, algorithm="HS256")
    return token


def decodeToken(encoded):
    try:
        token = jwt.decode(encoded, privatekey, algorithms=["HS256"])
        return token, False
    except:
        return None, True
