from django.db import models
import datetime
from django.utils import timezone
import math
import json
from DataStructures import *
# Create your models here.


##############
#  Initialize API's  #
##############

#Twilio
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException
account = "ACad5b697d43118d36082e78894c07fdbd"
token = "b625061400a44d2a8c8e0784412f8785"
client = TwilioRestClient(account, token)
FROM_NUMBER="+15308838474"

#GCM
from gcm import GCM
gcm = GCM("AIzaSyAUfP7ynnoS4BQGFm3ZybWtz9ns3n8TXYA")

#Yelp
import yelp

##############
#  managers  #
##############


class UserManager(models.Manager):
    def create_user(self, fid, friends, regId, pn):
        status = Status.objects.create_status()
        followers = Dicty.objects.create_dicty(fid+"'s followers")
        user = self.create(facebook_id=fid, friends=friends, status=status, regId=regId, phone_number = pn, followers=followers)
        user.sms=False
        #user.followers.name = fid+"'s followers"
        #user.followers.save()
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
    
    def subscriber(self, userid, type, topic, to):
        if type == 'add':
            for myuserid in to:
                if self.user_exists(myuserid):
                    user = self.get_user(myuserid)
                    user.appendkv(userid,topic)
                else:
                    print "ATTEMPTED TO SUBSCRIBE TO UNKNOWN USER: " + str(myuserid)
        elif type == 'delete':
            for myuserid in to:
                if self.user_exists(myuserid):
                    user = self.get_user(myuserid)
                    user.followers.deletekeyval(userid,topic)
                else:
                    print "ATTEMPTED TO DELETE SUBSCRIPTION TO UNKNOWN USER: " + str(myuserid)
        elif type == 'editfriends':
            return

class StatusManager(models.Manager):
    def create_status(self):
        status = self.create(status='', status_time= timezone.datetime.min, public=True)
        status.save()
        return status

class MeetingManager(models.Manager):
    def create_meeting(self, data):
        userid = data['userId']
        friendid = data['friendId']
        #ulat, ulong = data['userLocation']["latitude"], data['userLocation']["longitude"]
        #flat, flong = data['friendLocation']["latitude"], data['friendLocation']["longitude"]
        mname = data['meetingName']
        mlat, mlong = data['meetingLocation']["latitude"], data['meetingLocation']["longitude"]
        meeting = self.create(latitude=mlat, longitude=mlong, meeting_name = mname)
        meeting.friends = [userid, friendid]
        meeting.meeting_time = timezone.datetime.now()
        meeting.save()
        return meeting
    
    def get_meetings(self, ulat, ulong):
        ulocation = Location()
        ulocation.latitude, ulocation.longitude = ulat, ulong
        out = []
        for meeting in Meeting.objects.all():
            now = timezone.datetime.now()
            if now-meeting.meeting_time<datetime.timedelta(minutes=15):
                mlocation = Location()
                mlocation.latitude, mlocation.longitude = meeting.latitude, meeting.longitude
                dist = mlocation.get_distance(ulocation)
                if dist<10:
                    meetingdata = meeting.get_data()
                    out.append(meetingdata)
            else:
                meeting.delete() # IMPORTANT - THIS DELETES ALL MEETINGS THAT ARE OVER 15 MINS OLD
        return {'data':out}

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
            "ownId": friendid,
            "data": {
                "friendId": uid,
                "friendStatus": user.get_status(),
                "ownStatus": friend.get_status()
            }
        }
        
        gcmNotification(data, [friend.regId])
    
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
    print "notification payload:", data
    # data = {'data': data}
    response = gcm.json_request(registration_ids=reg_ids, data=data)
    print "submission response", response
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
    public = models.BooleanField()
    
    objects = StatusManager()
    
    def set_status(self, s, p):
        if p == 'true':
            self.public = True
        else:
            self.public = False
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
    phone_number = models.CharField(max_length=15)
    friends = ListField()
    followers = models.OneToOneField(Dicty)
    status = models.OneToOneField(Status)
    regId = models.CharField(max_length=4096)
    sms = models.BooleanField(default=False)
    
    objects = UserManager()
    
    def login(self, facebook_friends, regId):
        #self.sms('test_message')
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
                # print('user "' + friendid + '" has not yet joined friendzy')
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
    
    def set_status(self, status, public):
        self.status.set_status(status, public)
        self.notifyfollowers(status)
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
    
    def setsms(self, bools):
        print 'AT SETSMS METHOD, SETTING TO ' + str(bools)
        self.sms = bool(str(bools))
        self.save()
    
    def notifyfollowers(self, status):
        followers = self.followers.keyval_set.all()
        for follower in followers:
            userid = follower.key
            topic = follower.value
            if matches(topic, status) and User.objects.user_exists(userid):
                nuser = User.objects.get_user(userid)
                if nuser.sms:
                    notification_message = self.notification_message(self.facebook_id, status, topic)
                    nuser.send_sms(notification_message) #CHANGE LATER TO ALLOW FOR GCM/SMS BASED ON SETTINGS
                else:
                    data = {
                        "messageType": "initial",
                        "ownId": nuser.facebook_id,
                        "data": {
                            "friendId": self.facebook_id,
                            "friendStatus": nuser.get_status(),
                            "ownStatus": self.get_status()
                        }
                    }
                    gcmNotification(data, [nuser.regId])
    
    def notification_message(self, userid, status, topic):
        message = "user " + userid + " posted a message about '" + topic + "':  "
        message += '"' + status + '"'
        return message
    
    def send_sms(self, message):
        pn = self.phone_number
        print 'sending sms to '+pn+' which reads: '+message
        try:
            message = client.sms.messages.create(to=pn, from_=FROM_NUMBER, body=message)
        except TwilioRestException:
            "not a real phone number: " + pn
    
    def appendkv(self,userid,topic):
        self.followers.appendkv(userid,topic)
        self.save()
    
    @staticmethod
    def TESTAPI_resetFixture():
        User.objects.all().delete()
        Status.objects.all().delete()
        Appeal.objects.all().delete()
        Chat.objects.all().delete()
        KeyVal.objects.all().delete()
        Dicty.objects.all().delete()
        Meeting.objects.all().delete()

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
        
        message = {
            "messageType": "double",
            # Only necessary for initial when the respondent has to post his own id to server again
            "ownId": "NOT USED",
            "data": data
        }
        gcmNotification(message, [regId])
        
        # Switch around userId and friendId when sending to friend
        tmp = message["data"]["userId"]
        message["data"]["userId"] = message["data"]["friendId"]
        message["data"]["friendId"] = tmp
        gcmNotification(message, [User.objects.get_user(self.friendid).regId])
        
        #Create a Meeting object
        Meeting.objects.create_meeting(data)
        
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
        out['userId'] = user1id
        out['friendId'] = user2id
        out['userLocation'] = {"latitude":user1lat, "longitude":user1long}
        out['friendLocation'] = {"latitude":user2lat, "longitude":user2long}
        out['meetingName'] = meeting['name']
        out['meetingLocation'] = {"latitude":meeting['latitude'], "longitude":meeting['longitude']}
        return out
    
    @staticmethod
    def get_regId(uid):
        myuser = User.objects.get(facebook_id=uid)
        return myuser.regId
        

class Meeting(models.Model):
    #uid = models.CharField(max_length=200, default='')
    friends = ListField()
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    meeting_time = models.DateTimeField('meeting time', default=timezone.datetime.min)
    meeting_name = models.CharField(max_length=1000, default='')
    
    objects = MeetingManager()
    
    def get_data(self):
        #compute statuses
        statuses = []
        for userid in self.friends:
            statuses.append(User.objects.get_user(userid).get_status())
        #compute age
        ageinseconds = (self.meeting_time - datetime.datetime.now()).seconds
        age = ''
        if ageinseconds>60:
            age = str(ageinseconds//60) + " minutes"
        else:
            age = ageinseconds + " seconds"
        out = {}
        out['latitude'] = self.latitude
        out['longitude'] = self.longitude
        out['attendees'] = self.friends
        out['location_name'] = self.meeting_name
        out['match_age'] = age
        out['statuses'] = statuses
        return out

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
    
    def get_distance(self,l):
        lon1, lat1, lon2, lat2 = map(float,[self.longitude, self.latitude, l.longitude, l.latitude])
        print 'distances'
        print  lon1, lat1, lon2, lat2
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        km = 6367 * c
        print "DISTANCE IS " + str(km) + " km"
        return km 

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
        print "we have", i, "messages"
        while i>=0 and datetime.datetime.strptime(self.messages[i][1], '%Y-%m-%d %H:%M:%S.%f') >= lastvisit:
            message = self.messages[i][0]
            mydate = self.messages[i][1]
            msgs.append((message, mydate))
            i -= 1
        if msgs == []:
            msgs = [['']]
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
