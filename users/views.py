# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt                                          
from users.models import User, Status, Appeal
import friendzy
import json
import datetime


@csrf_exempt
def login(request):
    postrequest = json.loads(request.body)
    userID, facebookFriends, regId = postrequest['userID'], postrequest['facebookFriends'], postrequest['regId']
    myuser = None
    if not User.objects.user_exists(userID):
        myuser = User.objects.create_user(userID, facebookFriends, regId)
    else:
        myuser = User.objects.get_user(userID)
    friendStatuses = myuser.login(facebookFriends, regId)
    return HttpResponse(simplejson.dumps(friendStatuses), mimetype='application/json')

@csrf_exempt
def set_status(request):
    postrequest = json.loads(request.body)
    userID, status = postrequest['userID'], postrequest['status']
    if User.objects.user_exists(userID):
        myuser = User.objects.get_user(userID)
        matchingStatuses = myuser.set_status(status)
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
        print "USER " + str(userID) + " ACCEPTED APPEAL"
        appeal = Appeal.objects.get_appeal(userID, friendID)
        resp = appeal.notify(userLat, userLong)
        return HttpResponse(simplejson.dumps(resp), mimetype='application/json')
    else:
        appeal = Appeal.objects.create_appeal(userID, friendID, userLat, userLong)
        return HttpResponse(simplejson.dumps({'worked':'1'}), mimetype='application/json')










