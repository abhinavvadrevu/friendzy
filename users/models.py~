from django.db import models
import ast
import datetime
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




class User(models.Model):
    facebook_id = models.CharField(max_length=200)
    friends = ListField()
    status = models.CharField(max_length=200)
    status_time = models.DateTimeField('date published')
    
    @classmethod
    def login(cls, userid, facebook_friends):
        myuser = None
        try:
            myuser = User.objects.get(facebook_id=userid)
        except User.DoesNotExist:
            myuser = User()
            myuser.status_time = datetime.datetime.now() - datetime.timedelta(minutes=16)
            myuser.facebook_id = userid
            myuser.save()
        #user exists
        myuser.friends = facebook_friends
        myuser.save()
        return {"data":myuser.get_friend_statuses()}
    
    def get_friend_statuses(self):
        statuses = {}
        for friendid in self.friends:
            print 'id:'
            print friendid
            try:
                userid = friendid
                myuser = User.objects.filter(facebook_id=userid)
                if len(myuser) > 0:
                    myuser = myuser[0] # crappy filtering - can change to .get instead of .filter later
                else:
                    print("friend " + str(userid) + " not found in friendzy database!")
                    continue
                if myuser.get_status() != None:
                    statuses[myuser.facebook_id] = myuser.get_status()
            except User.DoesNotExist: #this except clause is only used when .filter is changed to .get
                #do nothing
                print("user " + str(self.facebook_id) + " needs to relogin to update friendlist")
        return statuses
    
    @classmethod
    def set_status(cls, userid, status, time):
        try:
            curuser = User.objects.get(facebook_id=userid)
            #user exists
            curuser.status = status
            status_time = curuser.parse_date(time)
            curuser.status_time = status_time
            curuser.save()
            statuses = curuser.get_friend_statuses()
            out = {}
            for key in statuses:
                if curuser.matches(status, statuses[key]):
                    out[key] = statuses[key]
            return out
        except User.DoesNotExist:
            print ('user does not exist!')

    def get_status(self):
        """
        returns status if valid, else returns None
        """
        now = datetime.datetime.now()
        statustime = self.status_time
        naive = statustime.replace(tzinfo=None)
        if now-naive < datetime.timedelta(minutes=15):
            return self.status
        return None
    
    @staticmethod
    def matches(string1, string2):
        """
        returns if string1 matches with string2
        more complex matching algorithm yet to come
        """
        return string1 == string2
    
    @staticmethod
    def parse_date(time):
        return time
    
    @staticmethod
    def TESTAPI_resetFixture():
        User.objects.all().delete()
    




