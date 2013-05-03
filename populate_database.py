import json
import urllib2

#burl = "http://friendzy.herokuapp.com"
burl = "http://127.0.0.1:8000"

def login(user, friends, regId, pn):
    data = json.dumps({"userID":user, "facebookFriends":friends, "regId":regId, "phone_number":pn})
    url = burl + '/login'
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    response=None
    try:
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, error:
        #print error.read()
        k= open('population_error.html','w')
        k.write(error.read())
        k.close()
    print response
    return json.loads(response)

def set_status(user, status, public):
    url = burl + '/set_status'
    data = json.dumps({"userID":user, "status":status, "is_public":public})
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    response=None
    try:
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, error:
        k= open('population_error.html','w')
        k.write(error.read())
        k.close()
    print response
    return json.loads(response)

def match(userid, friendid, userlat, userlong):
    url = burl + '/match'
    tosend = {}
    tosend['userID'] = userid
    tosend['friendID'] = friendid
    tosend['userLocation'] = {'latitude':userlat, 'longitude':userlong}
    data = json.dumps(tosend)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    response=None
    try:
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, error:
        k= open('population_error.html','w')
        k.write(error.read())
        k.close()
    print response
    return json.loads(response)

def chat(userid, friendid, msg, location):
    url = burl + '/chat'
    tosend = {}
    tosend['userID'] = userid
    tosend['friendID'] = friendid
    tosend['msg'] = msg
    tosend['meetup_location'] = location
    data = json.dumps(tosend)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    response=None
    try:
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, error:
        k= open('population_error.html','w')
        k.write(error.read())
        k.close()
    print response
    return json.loads(response)

def subscribe_update(userid, type, topic, to):
    url = burl + '/subscribe_update'
    tosend = {}
    tosend['userID'] = userid
    tosend['type'] = type
    tosend['subscribe_topic'] = topic
    tosend['subscribe_to'] = to
    data = json.dumps(tosend)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    response=None
    try:
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, error:
        k= open('population_error.html','w')
        k.write(error.read())
        k.close()
    print response
    return json.loads(response)

def sms(userid, sms):
    url = burl + '/set_sms'
    tosend = {}
    tosend['userID'] = userid
    tosend['sms'] = sms
    data = json.dumps(tosend)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    response=None
    try:
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, error:
        k= open('population_error.html','w')
        k.write(error.read())
        k.close()
    print response
    return json.loads(response)

def get_events(userid, latitude, longitude):
    url = burl + '/get_events'
    tosend = {}
    tosend['userID'] = userid
    tosend['userLocation'] = {}
    tosend['userLocation']['latitude'] = latitude
    tosend['userLocation']['longitude'] = longitude
    data = json.dumps(tosend)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    response=None
    try:
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, error:
        k= open('population_error.html','w')
        k.write(error.read())
        k.close()
    print response
    return json.loads(response)

def reset_fixture():
    url = burl + '/resetFixture'
    req = urllib2.Request(url)
    response = None
    try:
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, error:
        k= open('population_error.html','w')
        k.write(error.read())
        k.close()
    print response
    return response


#print 'reset_fixture'
#reset_fixture()
print ''

response  = get_events('c','42.477', '-122.087')