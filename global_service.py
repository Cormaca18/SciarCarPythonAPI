#!/usr/bin/python
# -*- coding: utf-8 -*-
import string
import random
import psycopg2
import math

def midpoint(x1,x2,y1,y2):
    ## little shortcut
    if x1 == y1: return [x1, (x2+y2)/2]
    if x2 == y2: return [(x1+y1)/2, x2]

    lon1, lat1 = radians(x1), radians(x2)
    lon2, lat2 = radians(y1), radians(y2)
    dLon = lon2-lon1

    Bx = cos(lat2) * cos(dLon)
    By = cos(lat2) * sin(dLon)
    lat3 = atan2(sin(lat1)+sin(lat2), sqrt((cos(lat1)+Bx)*(cos(lat1)+Bx) + By*By))
    lon3 = lon1 + atan2(By, cos(lat1) + Bx)
    return [degrees(lon3),degrees(lat3)]

def randomString(n):

    ans =  ''.join(str(chr(random.randint(97,122))) for i in range(n))
    return ans


def connectToDb(
    conn,
    dbname,
    dbhost,
    dbport,
    username,
    pwd,
):

    if conn == None or conn.closed:

        conn = psycopg2.connect(database=dbname, user=username,
                                password=pwd, host=dbhost,
                                port=str(dbport))

    return conn


def getDbCreds():

    database = 'd4hr3mhluv2dq6'
    user = 'jcmzowfovqlogd'
    password = \
        '467e3f5b20b8f853c022529d5944fc66cff8e5891df408023c8fb23596dcd23c'
    host = 'ec2-54-75-233-162.eu-west-1.compute.amazonaws.com'

    port = '5432'

    return {
        'dbName': database,
        'user': user,
        'pwd': password,
        'host': host,
        'port': port,
    }


def connectToMainDb(conn):
    dbCreds = getDbCreds()
    return connectToDb(
        conn,
        dbCreds['dbName'],
        dbCreds['host'],
        dbCreds['port'],
        dbCreds['user'],
        dbCreds['pwd'],
    )
