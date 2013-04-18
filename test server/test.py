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
        k= open('test.html','w')
        k.write(error.read())
        k.close()
    print response
    return json.loads(response)

def set_status(user, status, public):
    url = burl + '/set_status'
    data = json.dumps({"userID":user, "status":status, "public":public})
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    response=None
    try:
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, error:
        k= open('test.html','w')
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
        k= open('test.html','w')
        k.write(error.read())
        k.close()
    print response
    return json.loads(response)

def chat(userid, friendid, msg):
    url = burl + '/chat'
    tosend = {}
    tosend['userID'] = userid
    tosend['friendID'] = friendid
    tosend['msg'] = msg
    data = json.dumps(tosend)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    response=None
    try:
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, error:
        k= open('test.html','w')
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
        k= open('test.html','w')
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
        k= open('test.html','w')
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
        k= open('test.html','w')
        k.write(error.read())
        k.close()
    print response
    return response

#fid = '666900613'
#fid = '1'

print 'reset_fixture'
reset_fixture()
print ''

print 'Logging in first user'
fid, pn = 'a', "testnum"#"+19162762760"
print 'login'
response = login(fid, ['b','c','d','e'], fid, pn)
assert response == {"data": {}}, "login failed!"
print 'set_status'
response = set_status(fid, 'this is a test status1', 'true')
assert response == {'data':{}},  "status was not set correctly"
print ''


print 'Logging in second user'
fid = 'b'
print 'login'
response = login(fid, ['a','c','d', 'e'], fid, fid)
assert response == {"data": {"a": "this is a test status1"}}, 'login failed!'
print 'set_status'
response = set_status(fid, 'this is a test status1', 'false')
assert response == {"data": {"a": "this is a test status1"}}, 'status was not set correctly'
print 'matching'
print 'User a requesting match with user b'
response = match('a','b', "37.8717", "-122.2728")
assert response == {"worked": "1"}, 'matching failed'
print 'User b confirms match with user a'
response = match('b','a', "47.6097", "-122.3331")
assert response == {"worked": "1"}, 'matching failed'
print ''
print 'User a starts chat with user b'
response = chat('a','b','hi')
assert response == {"msg": [[""]], "senderID": "b", "connected": False}, 'chat sent'
print 'User b polls server for chats'
response = chat('b','a','')
assert response['msg'][0][0] == "hi", 'chat received'
print 'User b sends a message to user a'
response = chat('b','a','whats up')
assert response == {"msg": [[""]], "senderID": "a", "connected": True}, 'chat sent'


print 'Logging in third user'
fid = 'c'
print 'login'
response = login(fid, ['a','b','d'], fid, fid)
assert response == {"data": {"a": "this is a test status1", "b": "this is a test status1"}}, 'login failed'
print 'set_status'
response  = set_status(fid, 'is a test', 'true')
assert response == {"data": {"a": "this is a test status1", "b": "this is a test status1"}}, 'status was set correctly'
print 'User a subscribes to b and c'
response = subscribe_update('a','add','status',['b','c'])
assert response == {"worked": "1"}, 'subscribe failed'
print 'User a unsubscribes to c'
response = subscribe_update('a','delete','status',['c'])
assert response == {"worked": "1"}, 'unsubscribe failed'
print 'User b sets status'
response = set_status('b', 'test status2', 'true')
assert response  == {"data": {}}, 'status was not set correctly'

print 'User a turns on sms notifications'
response = sms('a','true')
assert response == {"worked": "1"}, 'sms turned on'
print 'User a turns off sms notifications'
response = sms('a','false')
assert response == {"worked": "1"}, 'sms turned off'
print 'User b sets status'
response = set_status('b', 'test status3', 'true')
assert response == {"data": {}}, 'status was not set correctly'
print 'User a sets status'
response = set_status('a', 'status3', 'true')
assert response == {"data": {"b": "test status3"}}, 'status was set correctly'
print 'User a requesting match with user c'
response = match('a','c', "37.879719", "-122.260744")
assert response == {"worked": "1"}, 'matching failed'
print 'User c subscribes to a and b'
response = subscribe_update('c','add','status',['b','a'])
assert response == {"worked": "1"}, 'subscribe failed'
print 'User b starts chat with user c'
response = chat('b','c','how are you?')
assert response == {"msg": [[""]], "senderID": "c", "connected": False}, 'chat sent'
print 'User b polls server for chats'
response = chat('c','b','')
assert response['msg'][0][0] == "how are you?", 'chat received'