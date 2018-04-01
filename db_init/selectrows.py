#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2

conn = psycopg2.connect(database='dbpnirefd12adi', user='wdayqvpehwopva'
                        ,
                        password='15e377137cee9ee465200640edf7b3f7d93c252a5d571026f2f139dbbbdb21db'
                        ,
                        host='ec2-54-75-225-143.eu-west-1.compute.amazonaws.com'
                        , port='5432')

cur = conn.cursor()

cur.execute('select * from CHATBOTS')

rows = cur.fetchall()

for elem in rows:
    print elem

conn.close()

			