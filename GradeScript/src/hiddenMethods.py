import hashlib

def generateHashKey(usrname,name,password):
    keyData = f"{usrname}:{name}:{password}".encode("utf-8")
    return hashlib.sha256(keyData).hexdigest()