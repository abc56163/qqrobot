from nonebot.default_config import *
import MySQLdb

HOST = '0.0.0.0'
PORT = '8086'

SUPERUSERS = {875472104}  # administrator qq
COMMAND_START = {'', '/', '!', '/-', '！'}  # exclude these opening characters as administrator commands


def base():
    db = MySQLdb.connect("10.245.0.224", "root", "58ganji@123", "58dh", charset='utf8')
    return db


def databases():
    db = base()
    try:
        db.ping()
    except:
        db = MySQLdb.connect("10.245.0.224", "root", "58ganji@123", "58dh", charset='utf8')
    return db