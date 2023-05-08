

# token design is simple. token = useremail+*tkn+id(in the database)
def getToken(id, email):
    token = email+"*tkn"+id
    return token


def decodeToken(token):
    try:
        err = False
        email = token.split("*tkn")[0]
        decoded = token.split("*tkn")[1]
        if email == "" or decoded == "":
            return None, True
        else:
            return decoded, err
    except:
        return None, True
