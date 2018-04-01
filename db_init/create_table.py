#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2



def createTables(c, con):

    c.execute("""CREATE TABLE USERS(
    USER_ID VARCHAR(40) PRIMARY KEY  NOT NULL,
    PHONE_NUMBER     VARCHAR(10) NOT NULL,
    NUM_TRIPS	    SMALLINT NOT NULL,
    NUM_CANCELS      SMALLINT NOT NULL,
    NUM_NOSHOWS      SMALLINT NOT NULL
    );
    """)

    c.execute("""CREATE TABLE TRIPS(
    TRIP_ID VARCHAR(30) PRIMARY KEY  NOT NULL,
    USER_ID          VARCHAR(40)  NOT NULL REFERENCES USERS(USER_ID),
    USERS_TICKED     VARCHAR(40)[] NOT NULL,
    START_TIME	     INT NOT NULL,
    END_TIME         INT NOT NULL,
    ORIGIN_LAT       REAL NOT NULL,
    ORIGIN_LONG      REAL NOT NULL,
    DEST_LAT         REAL NOT NULL,
    DEST_LONG        REAL NOT NULL,
    NUM_SEATS        SMALLINT  NOT NULL, 
    CANCELLED        BOOL NOT NULL,
    STATUS           SMALLINT NOT NULL
    );
    """)

    c.execute("""CREATE TABLE MATCHES(
    MATCH_ID VARCHAR(30) PRIMARY KEY  NOT NULL,
    TRIP1_ID         VARCHAR(30)  NOT NULL REFERENCES TRIPS(TRIP_ID),
    TRIP2_ID         VARCHAR(30)  NOT NULL REFERENCES TRIPS(TRIP_ID),
    MEETING_LAT      REAL NOT NULL,
    MEETING_LONG     REAL NOT NULL,
    SUCCESS          BOOL NOT NULL
    );
    """)


    con.commit()



def main():

    conn = psycopg2.connect(database='d4hr3mhluv2dq6', user='jcmzowfovqlogd'
                        ,
                        password='467e3f5b20b8f853c022529d5944fc66cff8e5891df408023c8fb23596dcd23c'
                        ,
                        host='ec2-54-75-233-162.eu-west-1.compute.amazonaws.com'
                        , port='5432')

    cur = conn.cursor()

    createTables(cur, conn)

    conn.close()

			
main()