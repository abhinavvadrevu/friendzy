# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt                                          
from users.models import User
import friendzy
import json
import datetime


@csrf_exempt
def login(request):
    print 'request here'
    print request.body
    postrequest = json.loads(request.body)
    userID = postrequest['userID']
    facebookFriends = postrequest['facebookFriends']
    friendStatuses = User.login(userID, facebookFriends)
    return HttpResponse(simplejson.dumps(friendStatuses), mimetype='application/json')

@csrf_exempt
def set_status(request):
    print 'request here'
    print request.body
    time = datetime.datetime.now()
    postrequest = json.loads(request.body)
    userID = postrequest['userID']
    status = postrequest['status']
    matchingStatuses = User.set_status(userID, status, time)
    return HttpResponse(simplejson.dumps(matchingStatuses), mimetype='application/json')

@csrf_exempt
def TESTAPI_resetFixture(request):
    User.TESTAPI_resetFixture()
    return HttpResponse(simplejson.dumps({'worked':'1'}), mimetype='application/json')
