#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import app
from flask import request
import json
import psycopg2
import global_service as gs
import json
from googleplaces import GooglePlaces, lang, types, Place
conn = None



@app.route('/no_show', methods=['POST'])
def no_show():
    #This function is called when a user does not show up
    global conn

    print("no show has occurred, updating user row")
    data = request.form
    print("got data")
    conn = gs.connectToMainDb(conn)
    print("connected to db")

    cur = conn.cursor()

    print("cursor created")

    print("sql done")
    print("data " + str(data))
    try:
        cur.execute('SELECT trip1_id, trip2_id FROM MATCHES WHERE match_id = %s', (data['match_id'],))
        returnedList = cur.fetchall()
        if data['trip_id']==returnedList[0][0]:
            cur.execute('SELECT user_id FROM trips WHERE trip_id = %s',
                        (returnedList[0][1],))
            bad_user = cur.fetchall()
            cur.execute('UPDATE users SET num_noshows = num_noshows + 1 WHERE user_id = %s',
                        (bad_user[0][0],))
            conn.commit()
            return '{"result":"success"}'
        else:
            cur.execute('SELECT user_id FROM trips WHERE trip_id = %s',
                        (returnedList[0][0],))
            bad_user = cur.fetchall()
            cur.execute('UPDATE users SET num_noshows = num_noshows + 1 WHERE user_id = %s',
                        (bad_user[0][0],))
            conn.commit()
            return '{"result":"success"}'

    except Exception as e:
        conn.close()
        return str(e)



@app.route('/met_match', methods=['POST'])
def met_match():
    #This function is called when a trip is successful
    global conn

    print("trip has been successful, updating user row")
    data = request.form
    print("got data")
    conn = gs.connectToMainDb(conn)
    print("connected to db")

    cur = conn.cursor()

    print("cursor created")

    print("sql done")
    print("data " + str(data))
    try:
        #removes the phone's trip id from the trips ticked list of the trip that they unticked
        cur.execute('UPDATE users SET num_trips = num_trips + 1 WHERE user_id = %s',
                    (data['user_id'],))
        conn.commit()
        return '{"result":"success"}'
    except Exception as e:
        print(str(e))
        return '{"result":"error"}'



@app.route('/cancelled', methods=['POST'])
def cancelled():
    #This function is called when a trip is cancelled
    global conn

    print("trip has been cancelled, updating user row")
    data = request.form
    print("got data")
    conn = gs.connectToMainDb(conn)
    print("connected to db")

    cur = conn.cursor()

    print("cursor created")

    print("sql done")
    print("data " + str(data))
    try:
        #removes the phone's trip id from the trips ticked list of the trip that they unticked
        cur.execute('UPDATE users SET num_cancels = num_cancels + 1 WHERE user_id = %s',
                    (data['user_id'],))
        conn.commit()
        return '{"result":"success"}'
    except Exception as e:
        print(str(e))
        return '{"result":"error"}'


@app.route('/trip_unticked', methods=['POST'])
def trip_unticked():
    #This function is called when a user unticks a trip
    global conn

    print("trip has been unticked, updating DB")
    data = request.form
    print("got data")
    conn = gs.connectToMainDb(conn)
    print("connected to db")

    cur = conn.cursor()

    print("cursor created")

    print("sql done")
    print("data " + str(data))
    try:
        #removes the phone's trip id from the trips ticked list of the trip that they unticked
        cur.execute('UPDATE trips SET trips_ticked = array_remove(trips_ticked, %s) WHERE trip_id = %s',
                    (data['phone_trip_id'], data['trip_id'],))
        conn.commit()
        return '{"result":"success",'+'"checkbox":"'+'False'+'"}'
    except Exception as e:
        print(str(e))
        return '{"result":"error"}'

@app.route('/submitTrip', methods=['POST'])
def submitTrip():
    #This function is called once a user submits a trip
    global conn

    print("submitting trip")


    data = request.form

    print("got data")

    conn = gs.connectToMainDb(conn)

    print("connected to db")

    cur = conn.cursor()

    print("cursor created")

    SQL = 'INSERT INTO TRIPS(TRIP_ID, USER_ID, TRIPS_TICKED, START_TIME, END_TIME, \
    ORIGIN_LAT, ORIGIN_LONG, DEST_LAT, DEST_LONG, NUM_SEATS, CANCELLED, STATUS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'

    print("sql done")
    #Trip ID is generated using the start and end time timestamps and a random string of length 6
    tripID = data['start_time'] + "%" +  data['end_time'] + "%" + gs.randomString(6)
    print(tripID)
    print("data " + str(data))

    try:
        #A new trip is created in the trips table in the database with the given information
        cur.execute(SQL, (tripID, data['user_id'], [], int(data['start_time']),
            int(data['end_time']), float(data['origin_lat']), float(data['origin_long']), float(data['dest_lat']),
            float(data['dest_long']), int(data['num_seats']), False, int(0),))

        conn.commit()
    except Exception as e:
        conn.close()
        print(str(e))
        return '{"result": "error"}'

    return '{"result":'+ tripID +'}'


@app.route('/submit_user', methods=['POST'])
def submit_user():
    #This function is called on first log in to add a new user to the user's table
    global conn

    print("submitting user")

    data = request.form

    print("got data "+str(data))
    #print("length "+ str('phone_number' in data))
    conn = gs.connectToMainDb(conn)

    print("connected to db")

    cur = conn.cursor()
    #Check if a number is already in the database for this user
    cur.execute('SELECT PHONE_NUMBER FROM USERS WHERE USER_ID=%s LIMIT 1', (data['user_id'],))
    userCheck = cur.fetchone()

    #Allow a user to use a different number
    if data['phone_number'] =="":
        cur.execute('SELECT PHONE_NUMBER FROM USERS WHERE USER_ID=%s LIMIT 1', (data['user_id'],))
        numberCheck = cur.fetchone()
        if numberCheck==None:
            return '{"result": "no number"}'
        else:
            return '{"result": "number updated"}'

    elif data['phone_number'] != "" and userCheck!=None:
        cur.execute('UPDATE users SET phone_number = %s WHERE user_id = %s', (data['phone_number'], data['user_id'],))
        conn.commit()
        return '{"result": "number updated"}'

    print("cursor created")
    SQL = 'INSERT INTO USERS(USER_ID, PHONE_NUMBER, NUM_TRIPS, NUM_CANCELS, NUM_NOSHOWS) VALUES (%s, %s, %s, %s, %s) \
        ON CONFLICT DO NOTHING;'
    print("sql done")
    print("data " + str(data))

    try:
        cur.execute(SQL, (data['user_id'], data['phone_number'], int(0), int(0), int(0),))
        conn.commit()
    except Exception as e:
        conn.close()
        print(str(e))
        return '{"result": "error"}'

    return '{"result": "success"}'



@app.route('/has_trip_matched', methods=['POST'])
def has_trip_matched():
    #This function is called every 5 seconds to see if a match has been made - instead of push notifications
    global conn

    print("checking for matched trip")
    data = request.form
    print("got data")
    conn = gs.connectToMainDb(conn)

    print("connected to db")

    cur = conn.cursor()

    print("cursor created")

    print("sql done")
    print("data " + str(data))
    #Takes a phone's trip id and sees if there has been a match made with this ID
    try:
        cur.execute('SELECT * FROM MATCHES WHERE TRIP1_ID = %s OR TRIP2_ID = %s', (data['trip_id'], data['trip_id'],))
        returnedList = cur.fetchall()
        if len(returnedList)==0:
            return '{"result":'+str([])+'}'
        else:
            return '{"result":'+json.dumps(returnedList[0][0])+'}'

    except Exception as e:
        conn.close()
        return str(e)


@app.route('/trip_ticked', methods=['POST'])
def trip_ticked():
    #Called when a user ticks a trip
    global conn
    API_KEY = 'AIzaSyD4WusmNjpBQ6TXXghBUR9AxQ5RtBpLPcE'
    google_places = GooglePlaces(API_KEY)

    print("trip has been ticked, updating DB")
    data = request.form
    print("got data")
    conn = gs.connectToMainDb(conn)
    print("connected to db")

    cur = conn.cursor()

    print("cursor created")

    print("sql done")
    print("data " + str(data))
    try:
        cur.execute('UPDATE trips SET trips_ticked = array_append(trips_ticked, %s) WHERE trip_id = %s and user_id != %s and %s != ALL(trips_ticked)',
                    (data['phone_trip_id'], data['trip_id'],data['user_id'],data['phone_trip_id'],))
        conn.commit()

        cur.execute('SELECT trips_ticked from trips where trip_id=%s', (data['phone_trip_id'],))

        checkingList = cur.fetchall()
        #print(checkingList[0][0])
        #print("phone trips ticked "+str(checkingList))
        print("got this far")
        print(str(checkingList))
        if checkingList!=[] and data['trip_id'] in checkingList[0][0]:
            #Once a user ticks a trip the API sees if a match has been made ie; they are in each other's lists
            #Returns all required info if so
            match_id = gs.randomString(25)
            print("adding match")
            cur.execute('select origin_lat, origin_long from trips where trip_id = %s', (data['phone_trip_id'],))
            phone_origin = cur.fetchall()
            cur.execute('select origin_lat, origin_long from trips where trip_id = %s', (data['phone_trip_id'],))
            trip_origin = cur.fetchall()
            midpoint = gs.midpoint(phone_origin[0][0],phone_origin[0][1],trip_origin[0][0],trip_origin[0][1])
            print("phone origin "+str(phone_origin))
            print("trip origin "+str(trip_origin))
            print("midpoint "+str(midpoint))
            types = ['restaurant', 'cafe', 'bank', 'meal_takeaway', 'convenience_store']
            for i in range(0,5):
                query_meetingPt = google_places.nearby_search(lat_lng={'lat': midpoint[0], 'lng': midpoint[1]},radius=15,type=types[i],
                                                                rankby='prominence')
                if len(str(query_meetingPt.raw_response['results']))>0:
                    break
            print("found")
            print(query_meetingPt.raw_response['results']==[])
            if query_meetingPt.raw_response['results']==[]:
                meetingPt = ""
            else:
                meetingPt = str(query_meetingPt.raw_response['results'][0]['name'])
            cur.execute('INSERT INTO matches(match_id, trip1_id, trip2_id, trip1_showed, trip2_showed, suggested_meeting_place) VALUES(%s, %s, %s, %s, %s, %s)',
                        (match_id, data['trip_id'], data['phone_trip_id'], False, False, meetingPt))
            conn.commit()
            return '{"result":"success",'+'"match":"'+match_id+'","checkbox":"'+'True",'+'"meeting_place":"'+meetingPt+'"}'
        else:
            match_id = []
            return '{"result":"success",'+'"match":"'+str(match_id)+'","checkbox":"'+'True",'+'"meeting_place":"'+'None'+'"}'
    except Exception as e:
        print(str(e))
        return '{"result":"error"}'


@app.route('/get_potential_matches', methods=['POST'])
def get_potential_matches():
    #Get potential matches function
    #Not ranked yet
    API_KEY = 'AIzaSyD4WusmNjpBQ6TXXghBUR9AxQ5RtBpLPcE'
    google_places = GooglePlaces(API_KEY)
    global conn

    print("checking for potential matches")
    data = request.form
    print("got data")

    conn = gs.connectToMainDb(conn)
    print("connected to db")

    cur = conn.cursor()
    print("cursor created")
    cur.execute('select trip_id, start_time, end_time, user_id, trips_ticked from trips where trip_id=%s', (data['trip_id'],))
    #print(cur.query)
    thistripData = cur.fetchall()
    print(thistripData)
    #print("data " + str(data))
    if thistripData==[]:
        return '{"result": "not a valid trip"}'

    try:
        cur.execute('select * from trips where trip_id != %s and user_id!=%s and ((%s between start_time and end_time) or (start_time between %s and %s))',
        (thistripData[0][0],thistripData[0][3], thistripData[0][1], thistripData[0][1], thistripData[0][2],))
        ansr = cur.fetchall()
        mylist = []
        print(str(ansr))
        for i in range(len(ansr)):
            HM = {}
            AM = {}
            HM["origin_lat"] = str(ansr[i][5])
            HM["origin_long"] = str(ansr[i][6])
            HM["dest_lat"] = str(ansr[i][7])
            HM["dest_long"] =str(ansr[i][8])
            
            query_origin = google_places.nearby_search(lat_lng={'lat': HM["origin_lat"], 'lng': HM["origin_long"]},radius=20)
            query_dest = google_places.nearby_search(lat_lng={'lat': HM["dest_lat"], 'lng': HM["dest_long"]},radius=20)
            if len(query_origin.raw_response['results'][0]['name']) and len(query_dest.raw_response['results'][0]['name']) > 0:
                AM["origin"] = str(query_origin.raw_response['results'][0]['name'])
                AM["dest"] = str(query_dest.raw_response['results'][0]['name'])
            else:
                AM["origin"] = []
                AM["dest"] = []
            
            AM["origin"] = "GREG"
            AM["dest"] = "PECK"


            AM["num_seats"] = str(ansr[i][9])
            if thistripData[0][0] in ansr[i][2]:
                print("here "+str(ansr[i][2]))
                AM["checked"] = True
            else:
                print("here "+str(ansr[i][2]))
                AM["checked"] = False
            if ansr[i][0] in thistripData[0][4]:
                AM["circle"] = True
            else:
                AM["circle"] = False
            AM["trip_id"] = ansr[i][0]
            mylist.append(AM)

        #print(str(query_dest.raw_response['results'][0]['name']))
        #print(str(query_dest.raw_response))
        return '{"result": "success", "trips":'+json.dumps(mylist)+'}'
    except Exception as d:
        print(str(d))
        return '{"result": "error"}'
