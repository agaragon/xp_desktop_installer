from json import load, dumps, loads
from cryptography.fernet import Fernet
from os.path import join
from sys import path

key = b'1GsKHeGRlS3HcvgCtK5mimWaJBxI2EBDGYAACY9A9TY='
cryptographer = Fernet(key)


def get_server_from_email(email):
    return("smtp."+email.split("@")[1])


def encode_json_conf(conf):
    new_conf = dumps(conf)
    encoded_new_conf = str(cryptographer.encrypt(new_conf.encode()), 'UTF-8')
    return encoded_new_conf
