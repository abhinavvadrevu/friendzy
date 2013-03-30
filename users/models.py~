from django.db import models
import ast
import datetime
from django.utils import timezone
import math
import yelp
import json
# Create your models here.


class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"
    
    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)
    
    def to_python(self, value):
        if not value:
            value = []
        if isinstance(value, list):
            return value
        return ast.literal_eval(value)
    
    def get_prep_value(self, value):
        if value is None:
            return value
        return unicode(value)
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class Status(models.Model):
    
    status = models.CharField(max_length=200, default = '')
    status_time = models.DateTimeField('date published', default=timezone.datetime.min)
    
    def set_status(self, s):
        self.status = s
        self.status_time = timezone.datetime.now()
        self.save()
    def get_status(self):
        now = timezone.datetime.now()
        if now-self.status_time<datetime.timedelta(minutes=15):
            return self.status
        return None


class UserManager(models.Manager):
    def create_user(self, fid, friends):
        status = Status()
        status.set_status('')
        return self.create(facebook_id=fid, friends=friends, status=status)


class User(models.Model):
    facebook_id = models.CharField(max_length=200)
    friends = ListField()
    status = models.OneToOneField(Status)
    
    objects = UserManager()
    
    @classmethod
    def user_exists(cls, fid):
        try:
            User.objects.get(facebook_id=fid)
        except User.DoesNotExist:
            return False
        except User.MultipleObjectsReturned: #SHOULD NEVER HAPPEN! ONLY USEFUL FOR DEBUGGING.
            return True
        return True
    
    def login(self, facebook_friends):
        self.friends = facebook_friends
        self.save()
        return {"data":self.get_friend_statuses()}
    
    def get_friend_statuses(self):
        statuses = {}
        for friendid in self.friends:
            try:
                myuser = User.objects.get(facebook_id=friendid)
            except User.DoesNotExist:
                #do nothing
                print('user "' + friendid + '" has not yet joined friendzy')
                continue
            except User.MultipleObjectsReturned: #THIS CLAUSE IS FOR DEBUGGING ONLY!
                #get one of the users
                #NOTE THIS SHOULD NOT HAPPEN BUT THIS CASE IS USEFUL WHILE DEBUGGING
                print 'MULTIPLE USERS WITH ID "' + friendid + '"'
                myuser = User.objects.filter(facebook_id=friendid)
                myuser = myuser[0]
            else:
                if myuser.get_status() != None:
                    statuses[myuser.facebook_id] = myuser.get_status()
        return statuses
    
    def set_status(self, status):
        self.status.set_status(status)
        #self.save()
        #return matching statuses
        fstatuses = self.get_friend_statuses()
        out = {}
        for fid in fstatuses:
            fstatus = fstatuses[fid]
            if matches(fstatus, status):
                out[fid] = fstatus
        return {"data": out}
    
    def get_status(self):
        return self.status.get_status()
    
    @staticmethod
    def TESTAPI_resetFixture():
        User.objects.all().delete()
        Status.objects.all().delete()

def matches(string1, string2):
    """
    returns if string1 matches with string2
    more complex matching algorithm yet to come
    """
    return string1 in string2 or string2 in string1


class Location(models.Model):
    
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    
    def midpoint(self, l):
        lat1 = self.latitude
        long1 = self.longitude
        lat2 = l.latitude
        long2 = l.longitude
        lonA = math.radians(long1)
        lonB = math.radians(long2)
        latA = math.radians(lat1)
        latB = math.radians(lat2)
        dLon = lonB - lonA
        Bx = math.cos(latB) * math.cos(dLon)
        By = math.cos(latB) * math.sin(dLon)
        latC = math.atan2(math.sin(latA) + math.sin(latB), math.sqrt((math.cos(latA) + Bx) * (math.cos(latA) + Bx) + By * By))
        lonC = lonA + math.atan2(By, math.cos(latA) + Bx)
        lonC = (lonC + 3 * math.pi) % (2 * math.pi) - math.pi
        lat3, long3 = (math.degrees(latC), math.degrees(lonC))
        out = Location()
        out.latitude = lat3
        out.longitude = long3
        return out
    
    def get_meeting_point(self,l):
        midlocation = self.midpoint(l)
        a,b = midlocation.latitude, midlocation.longitude
        url_params = {}
        url_params['term'] = 'restaurant'
        url_params['ll'] = str(a) + ',' + str(b)
        url_params['limit'] = '1'
        response = yelp.request('api.yelp.com', '/v2/search', url_params, "AeLIHzyGSsi0QdhpvbM-Ug", "pJudUhIyHj4AuTXntrO_xAksyFI", "40HMWzBg-Zb0I9Wnbt6zVDte7BD6sHEB", "4a_1hN7NpD4JkMEtwuasp8lt0kA")
        #print type(response)
        #print response
        respdict = response#json.loads(response)
        out = {}
        out['address'] = reduce(lambda x, y: x+ ' ' + y, respdict['businesses'][0]['location']['display_address'])
        out['latitude'] = respdict['businesses'][0]['location']['coordinate']['latitude']
        out['longitude'] = respdict['businesses'][0]['location']['coordinate']['longitude']
        out['name'] = respdict['businesses'][0]['name']
        return {'data': out}
