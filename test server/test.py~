import json
import urllib2

#burl = "http://friendzy.herokuapp.com"
burl = "http://127.0.0.1:8000"

def login(user, friends):
    data = json.dumps({"userID":user, "facebookFriends":friends})
    url = burl + '/login'
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    response=None
    try:
        f = urllib2.urlopen(req)
        response = f.read()
        print 'asdf'
        f.close()
    except urllib2.HTTPError, error:
        print error.read()
        k= open('test.html','w')
        k.write(error.read())
        k.close()
    print 'a'
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


fid = '588985867'
fid = '1'
login(fid, ['b','c','d'])
set_status(fid, 'this is a test status1')

print '2'


fid = 'b'
login(fid, ['1','c','d'])
set_status(fid, 'this is a test status1')



