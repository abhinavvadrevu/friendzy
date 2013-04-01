# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt                                          
from users.models import User
import friendzy
import json
import datetime
from gcm import GCM


@csrf_exempt
def login(request):
    postrequest = json.loads(request.body)
    userID, facebookFriends = postrequest['userID'], postrequest['facebookFriends']
    myuser = None
    if not User.user_exists(userID):
        myuser = User.objects.create_user(userID, facebookFriends)
    else:
        myuser = User.objects.get(facebook_id=userID)
    friendStatuses = myuser.login(facebookFriends)
    return HttpResponse(simplejson.dumps(friendStatuses), mimetype='application/json')

@csrf_exempt
def set_status(request):
    postrequest = json.loads(request.body)
    userID, status = postrequest['userID'], postrequest['status']
    if User.user_exists(userID):
        myuser = User.objects.get(facebook_id=userID)
        matchingStatuses = myuser.set_status(status)
        return HttpResponse(simplejson.dumps(matchingStatuses), mimetype='application/json')
    return HttpResponse(simplejson.dumps({'errCode':-1, 'data':'USER DOES NOT EXIST'}), mimetype='application/json')

def TESTAPI_resetFixture(request):
    User.TESTAPI_resetFixture()
    return HttpResponse(simplejson.dumps({'worked':'1'}), mimetype='application/json')

@csrf_exempt
def gcmtest(request):
    postrequest = json.loads(request.body)
    gcm = GCM("AIzaSyAUfP7ynnoS4BQGFm3ZybWtz9ns3n8TXYA")
    data = {'data': 'IT WORKED!', 'param2': 'value2'}
    reg_ids = [postrequest['regId']]
    response = gcm.json_request(registration_ids=reg_ids, data=data)
    print response
    return HttpResponse(simplejson.dumps({'worked':'1'}), mimetype='application/json')
