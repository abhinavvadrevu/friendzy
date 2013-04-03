from django.db import models
import datetime
from django.utils import timezone
import math
import yelp
import json
from gcm import GCM
from ListField import ListField
# Create your models here.

##############
#  managers  #
##############


class UserManager(models.Manager):
    def create_user(self, fid, friends, regId):
        status = Status.objects.create_status()
        user = self.create(facebook_id=fid, friends=friends, status=status, regId=regId)
        user.save()
        return user
    
    def user_exists(self, fid):
        try:
            User.objects.get(facebook_id=fid)
        except User.DoesNotExist:
            return False
        except User.MultipleObjectsReturned: #SHOULD NEVER HAPPEN! ONLY USEFUL FOR DEBUGGING.
            return True
        return True
    
    def get_user(self, fid):
        return User.objects.get(facebook_id=fid)

class StatusManager(models.Manager):
    def create_status(self):
        status = self.create(status='', status_time= timezone.datetime.min)
        status.save()
        return status

class AppealManager(models.Manager):
    def create_appeal(self, uid, friendid, latitude, longitude):
        self.create(uid=uid, friendid = friendid, latitude=float(latitude), longitude=float(longitude))
        print "USER " + str(uid) + " CREATED APPEAL, REQUESTING MATCH WITH USER " + str(friendid)
        #notify friend of potential match
        self.notify(uid, friendid)
    
    def notify(self, uid, friendid):
        """
        Notify friendId that uid has appealed them.
        
        This is ***DIFFERENT*** from Appeal.notify() which notifies a ***CONFIRMED*** match
        """
        user = User.objects.get_user(uid)
        friend = User.objects.get_user(friendid)
        
        data = {
            "messageType": "initial",
            "data": {
                "friendID": uid,
                "friendStatus": user.status
            }
        }
        
        gcmNotification(data, [f.regId])
    
    def appeal_exists(self, user1, user2):
        try:
            appeal = Appeal.objects.get(uid=user1, friendid=user2)
        except Appeal.DoesNotExist:
            try:
                appeal = Appeal.objects.get(uid=user2, friendid=user1)
            except Appeal.DoesNotExist:
                return False
            else:
                return True
        else:
            return True
    
    def get_appeal(self, user1, user2):
        try:
            appeal = Appeal.objects.get(uid=user1, friendid=user2)
        except Appeal.DoesNotExist:
                appeal = Appeal.objects.get(uid=user2, friendid=user1)
                return appeal
        else:
            return appeal

class ChatManager(models.Manager):
    def create_chat(self, userID, friendID):
        chat = self.create(user1id=userID, user2id=friendID)
        chat.save()
        return chat
    
    def chat_exists(self, userID, friendID):
        try:
            chat = Chat.objects.get(user1id=userID, user2id=friendID)
        except Chat.DoesNotExist:
            try:
                chat = Chat.objects.get(user1id=friendID, user2id=userID)
            except Chat.DoesNotExist:
                return False
            else:
                return True
        else:
            return True
    
    def get_chat(self, userID, friendID):
        try:
            chat = Chat.objects.get(user1id=userID, user2id=friendID)
        except Chat.DoesNotExist:
                chat = Chat.objects.get(user1id=friendID, user2id=userID)
                return chat
        else:
            return chat

####################
#  misc functions  #
####################

def matches(string1, string2):
    """
    returns True if string1 matches with string2
    more complex matching algorithm yet to come
    """
    return string1 in string2 or string2 in string1

def gcmNotification(data, reg_ids):
    gcm = GCM("AIzaSyAUfP7ynnoS4BQGFm3ZybWtz9ns3n8TXYA")
    print data
    data = {'data': data}
    response = gcm.json_request(registration_ids=reg_ids, data=data)
    print response
    return {'worked':'1'}

############
#  models  #
############

class Status(models.Model):
    """
    Status class for storing statuses
    """
    status = models.CharField(max_length=200, default = '')
    status_time = models.DateTimeField('date published', default=timezone.datetime.min)
    
    objects = StatusManager()
    
    def set_status(self, s):
        self.status = s
        self.status_time = timezone.datetime.now()
        self.save()
    def get_status(self):
        now = timezone.datetime.now()
        if now-self.status_time<datetime.timedelta(minutes=15):
            return self.status
        return None

class User(models.Model):
    """
    User class
    """
    facebook_id = models.CharField(max_length=200)
    friends = ListField()
    status = models.OneToOneField(Status)
    regId = models.CharField(max_length=4096)
    
    objects = UserManager()
    
    def login(self, facebook_friends, regId):
        self.friends = facebook_friends
        self.regId = regId
        self.save()
        #return {"data":{str(self.friends[0]):"status1", str(self.friends[1]):"status2", str(self.friends[2]):"status3", str(self.friends[3]):"status4"}} # for testing frontend only
        return {"data":self.get_friend_statuses()}
    
    def get_friend_statuses(self):
        """
        returns all friends' statuses
        """
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
        #return {"data":{"friend1":"status1", "friend2":"status2", "friend3":"status3", "friend4":"status4"}} # for testing frontend only
        return {"data": out}
    
    def get_status(self):
        return self.status.get_status()
    
    @staticmethod
    def TESTAPI_resetFixture():
        User.objects.all().delete()
        Status.objects.all().delete()
        Appeal.objects.all().delete()
        Chat.objects.all().delete()

class Appeal(models.Model):
    """
    Appeal class
    """
    uid = models.CharField(max_length=200, default='')
    friendid = models.CharField(max_length=200, default='')
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    
    objects = AppealManager()
    
    def notify(self, flat, flong):
        """
        notifies CONFIRMED match
        NOTE THIS IS DIFFERENT FROM AppealManager.notify() WHICH NOTIFIES A POTENTIAL MATCH
        """
        data = self.get_data(self.friendid, flat, flong)
        regId = Appeal.get_regId(self.uid)
        gcmNotification({'data':data, "messageType": "double"}, [regId, User.objects.get_user(friendid).regId])
        print "USER " + str(self.uid) + " NOTIFIED, deleting appeal"
        self.delete()
        
        return {'worked':'1'}
    
    def get_data(self, fuid1, flatitude1, flongitude1):
        user1id, user1lat, user1long = self.uid, self.latitude, self.longitude
        user2id, user2lat, user2long = fuid1, flatitude1, flongitude1
        user1loc = Location()
        user2loc = Location()
        user1loc.set_location(user1lat, user1long)
        user2loc.set_location(user2lat, user2long)
        meeting = user1loc.get_meeting_point(user2loc)
        out = {}
        out['userID'] = user1id
        out['userLocation'] = {"latitude":user1lat, "longitude":user1long}
        out['friendLocation'] = {"latitude":user2lat, "longitude":user2long}
        out['meetingName'] = meeting['name']
        out['meetingLocation'] = {"latitude":meeting['latitude'], "longitude":meeting['longitude']}
        return out
    
    @staticmethod
    def get_regId(uid):
        myuser = User.objects.get(facebook_id=uid)
        return myuser.regId
        

class Location(models.Model):
    """
    Location class
    """
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    
    def set_location(self, latitude, longitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)
    
    def midpoint(self, l):
        lat1, long1 = self.latitude, self.longitude
        lat2, long2 = l.latitude, l.longitude
        lonA, lonB = math.radians(long1), math.radians(long2)
        latA, latB = math.radians(lat1), math.radians(lat2)
        dLon = lonB - lonA
        Bx = math.cos(latB) * math.cos(dLon)
        By = math.cos(latB) * math.sin(dLon)
        latC = math.atan2(math.sin(latA) + math.sin(latB), math.sqrt((math.cos(latA) + Bx) * (math.cos(latA) + Bx) + By * By))
        lonC = lonA + math.atan2(By, math.cos(latA) + Bx)
        lonC = (lonC + 3 * math.pi) % (2 * math.pi) - math.pi
        out = Location()
        out.latitude, out.longitude = (math.degrees(latC), math.degrees(lonC))
        return out
    
    def get_meeting_point(self,l):
        midlocation = self.midpoint(l)
        a,b = midlocation.latitude, midlocation.longitude
        url_params = {}
        url_params['term'] = 'restaurant'
        url_params['ll'] = str(a) + ',' + str(b)
        url_params['limit'] = '1'
        respdict = yelp.request('api.yelp.com', '/v2/search', url_params, "AeLIHzyGSsi0QdhpvbM-Ug", "pJudUhIyHj4AuTXntrO_xAksyFI", "40HMWzBg-Zb0I9Wnbt6zVDte7BD6sHEB", "4a_1hN7NpD4JkMEtwuasp8lt0kA")
        out = {}
        out['address'] = reduce(lambda x, y: x+ ' ' + y, respdict['businesses'][0]['location']['display_address'])
        out['latitude'] = respdict['businesses'][0]['location']['coordinate']['latitude']
        out['longitude'] = respdict['businesses'][0]['location']['coordinate']['longitude']
        out['name'] = respdict['businesses'][0]['name']
        print out
        return out

class Chat(models.Model):
    """
    Location class
    """
    messages = ListField()
    user1id = models.CharField(max_length=200)
    user2id = models.CharField(max_length=200)
    user1lastvisit  = models.DateTimeField('user 1 last visit', default=timezone.datetime.min)
    user2lastvisit  = models.DateTimeField('user 2 last visit', default=timezone.datetime.min)
    
    objects = ChatManager()
    
    def add_message(self, userID, message):
        self.messages.append((message, str(timezone.datetime.now()), userID))
        self.save()
    
    def get_updates(self, friendID):
        lastvisit = None
        if friendID == self.user1id:
            lastvisit = self.user2lastvisit
        else:
            lastvisit = self.user1lastvisit
        msgs, i = [], len(self.messages)-1
        while i>=0 and datetime.datetime.strptime(self.messages[i][1], '%Y-%m-%d %H:%M:%S.%f') >= lastvisit:
            message = self.messages[i][0]
            mydate = self.messages[i][1]
            msgs.append((message, mydate))
            i -= 1
        if msgs == []:
            msgs = ['']
        return msgs
    
    def visited(self, userID):
        if userID == self.user1id:
            self.user1lastvisit = timezone.datetime.now()
        else:
            self.user2lastvisit = timezone.datetime.now()
        self.save()
    
    def connected(self, userID):
        lastvisit = None
        if userID == self.user1id:
            lastvisit = self.user1lastvisit
        else:
            lastvisit = self.user2lastvisit
        return timezone.datetime.now() - lastvisit < datetime.timedelta(seconds=10)
