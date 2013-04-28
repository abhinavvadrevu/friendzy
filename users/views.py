# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt                                          
from users.models import User, Status, Appeal, Chat, Meeting
import friendzy
import json
import datetime
from gcm import GCM


@csrf_exempt
def login(request):
    postrequest = json.loads(request.body)
    userID, facebookFriends, regId, pn = postrequest['userID'], postrequest['facebookFriends'], postrequest['regId'], postrequest['phone_number']
    myuser = None
    if not User.objects.user_exists(userID):
        myuser = User.objects.create_user(userID, facebookFriends, regId, pn)
    else:
        myuser = User.objects.get_user(userID)
    friendStatuses = myuser.login(facebookFriends, regId)
    return HttpResponse(simplejson.dumps(friendStatuses), mimetype='application/json')

@csrf_exempt
def set_status(request):
    postrequest = json.loads(request.body)
    userID, status, public = postrequest['userID'], postrequest['status'], postrequest['is_public']
    if User.objects.user_exists(userID):
        myuser = User.objects.get_user(userID)
        matchingStatuses = myuser.set_status(status, public)
        return HttpResponse(simplejson.dumps(matchingStatuses), mimetype='application/json')
    return HttpResponse(simplejson.dumps({'errCode':-1, 'data':'USER DOES NOT EXIST'}), mimetype='application/json')

def TESTAPI_resetFixture(request):
    User.TESTAPI_resetFixture()
    return HttpResponse(simplejson.dumps({'worked':'1'}), mimetype='application/json')

@csrf_exempt
def match(request):
    postrequest = json.loads(request.body)
    userID = postrequest['userID']
    friendID = postrequest['friendID']
    userLat = postrequest['userLocation']['latitude']
    userLong = postrequest['userLocation']['longitude']
    if Appeal.objects.appeal_exists(userID, friendID):
        print "user", userID, "accepted", friendID, "'s appeal"
        appeal = Appeal.objects.get_appeal(userID, friendID)
        resp = appeal.notify(userLat, userLong)
        return HttpResponse(simplejson.dumps(resp), mimetype='application/json')
    else:
        print "created appeal from", userID, "to", friendID
        appeal = Appeal.objects.create_appeal(userID, friendID, userLat, userLong)
        return HttpResponse(simplejson.dumps({'worked':'1'}), mimetype='application/json')

@csrf_exempt
def chat(request):
    postrequest = json.loads(request.body)
    userID = postrequest['userID']
    friendID = postrequest['friendID']
    msg = postrequest['msg']
    meetup_location = postrequest['meetup_location']
    if not Chat.objects.chat_exists(userID, friendID):
        print "chat doesn't exist, creating"
        Chat.objects.create_chat(userID, friendID)
    chat = Chat.objects.get_chat(userID, friendID)
    outmsgs = chat.get_updates(friendID)
    if not msg == '':
        print "adding message:", msg
        chat.add_message(userID, msg)
    connected = chat.connected(friendID)
    chat.visited(userID)
    meeting_location = Meeting.objects.update_meetup(userID, friendID, meetup_location) #udate and get latest meetup!
    data = {'msg':outmsgs, 'connected':connected, 'senderID':friendID, "current_meetup_location":meeting_location}
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')
        
@csrf_exempt
def subscribe_update(request):
    postrequest = json.loads(request.body)
    userID, type, topic, to = postrequest['userID'], postrequest['type'], postrequest['subscribe_topic'], postrequest['subscribe_to']
    if User.objects.user_exists(userID):
        User.objects.subscriber(userID, type, topic, to)
        return HttpResponse(simplejson.dumps({'worked':'1'}), mimetype='application/json')
    return HttpResponse(simplejson.dumps({'errCode':-1, 'data':'USER DOES NOT EXIST'}), mimetype='application/json')

@csrf_exempt
def set_sms(request):
    postrequest = json.loads(request.body)
    userID, sms = postrequest['userID'], postrequest['sms']
    if User.objects.user_exists(userID):
        user = User.objects.get_user(userID)
        user.setsms(sms)
        return HttpResponse(simplejson.dumps({'worked':'1'}), mimetype='application/json')
    return HttpResponse(simplejson.dumps({'errCode':-1, 'data':'USER DOES NOT EXIST'}), mimetype='application/json')

@csrf_exempt
def get_events(request):
    postrequest = json.loads(request.body)
    userID = postrequest['userID']
    userLat = postrequest['userLocation']['latitude']
    userLong = postrequest['userLocation']['longitude']
    meetings = Meeting.objects.get_meetings(userLat, userLong)
    return HttpResponse(simplejson.dumps(meetings), mimetype='application/json')

@csrf_exempt
def gcmtest(request):
    regId = postrequest['regId']
    gcm = GCM("AIzaSyAUfP7ynnoS4BQGFm3ZybWtz9ns3n8TXYA")
    data = {'data': {'worked':'1'}}
    response = gcm.json_request(registration_ids=reg_ids, data=data)
    return HttpResponse(simplejson.dumps({'worked':'1'}), mimetype='application/json')



