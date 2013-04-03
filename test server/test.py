import json
import urllib2

#burl = "http://friendzy.herokuapp.com"
burl = "http://127.0.0.1:8000"

def login(user, friends, regId):
    data = json.dumps({"userID":user, "facebookFriends":friends, "regId":regId})
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
    return response

def set_status(user, status):
    url = burl + '/set_status'
    data = json.dumps({"userID":user, "status":status})
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
    return response

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
    return response

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
    return response

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

"""
print 'Logging in first user'
fid = 'a'
print 'login'
login(fid, ['b','c','d','e'], fid)
print 'set_status'
set_status(fid, 'this is a test status1')
print ''

print 'Logging in second user'
fid = 'b'
print 'login'
login(fid, ['a','c','d', 'e'], fid)
print 'set_status'
set_status(fid, 'test status1')
print ''

print 'User a requesting match with user b'
match('a','b', "37.8717", "-122.2728")
print 'User b confirms match with user a'
match('b','a', "47.6097", "-122.3331")
print ''

print 'User a starts chat with user b'
chat('a','b','hi')
print 'User b polls server for chats'
chat('b','a','')
print 'User b sends a message to user a'
chat('b','a','whats up')



print 'Logging in third user'
fid = 'c'
print 'login'
login(fid, ['a','b','d'], fid)
print 'set_status'
set_status(fid, 'is a test')


"""
