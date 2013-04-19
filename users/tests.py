"""
    This file demonstrates writing tests using the unittest module. These will pass
    when you run "manage.py test".
    
    Replace this with more appropriate tests for your application.
    """
import sys, os
sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path
import unittest
from users import models


class UserTest(unittest.TestCase):
    
    #@patch('models.User.get_friend_statuses')
    def test_user_exists(self):
        # objects.create creates and saves a db entry in one step
        models.User.objects.create_user('an_id', ['some', 'list', 'items'],'123', '1234567')
        self.assertTrue(models.User.objects.user_exists('an_id'),"user_exists test fails")
        
    def test_user_exists1(self):
        # objects.create creates and saves a db entry in one step
        models.User.objects.create_user('user1', ['some', 'list', 'items'],'123', '1234567')
        self.assertTrue(models.User.objects.user_exists('user1'),"user doesn't not exit")
  
    def test_Status(self):
        status1 = models.Status()
        ans = "ABC"
        status1.set_status(ans,True)
        self.assertEqual(status1.status, ans)
    
    def test_Status2(self):
        status1 = models.Status()
        status2 = models.Status()
        ans = "ABC"
        wrong = '123'
        status1.set_status(ans,True)
        self.assertNotEqual(status1.status, wrong)
    
    def test_Status3(self):
        status1 = models.Status()
        ans = "ABC"
        status1.set_status(ans,True)
        self.assertEqual(status1.get_status(), ans)
        
    def test_chat1(self):
        models.Chat.objects.create_chat('userID', 'friendID')
        self.assertTrue(models.Chat.objects.chat_exists('userID', 'friendID'), ' chat not exists')
        
    def test_chat2(self):
        models.Chat.objects.create_chat('userID', 'friendID')
        self.assertFalse(models.Chat.objects.chat_exists('userID1', 'friendID'), 'chat fail: wrong user ID')
        
    def test_chat3(self):
        models.Chat.objects.create_chat('userID', 'friendID')
        self.assertFalse(models.Chat.objects.chat_exists('userID', 'friendID1'), 'chat fail: wrong friend ID')
    
    def test_matching_status(self):
        status1 = 'abc'
        status2 = 'abc'
        self.assertTrue(models.matches(status1, status2),"matching is not correct")
    
    def test_matching_status1(self):
        status1 = 'abc'
        status2 = 'def'
        self.assertFalse(models.matches(status1, status2),"matching is correct")
    
    def test_status_from_user(self):
        user5 = models.User()
        user5.status = models.Status()
        user5.status.set_status('123', True)
        self.assertEqual(user5.status.status, '123')
    
    def test_status_from_user1(self):
        user5 = models.User()
        user5.status = models.Status()
        user5.status.set_status('123', True)
        self.assertNotEqual(user5.status.get_status(), '456')

    def test_fbID(self):
        user = models.User()
        models.User.objects.create_user('an_id', ['some', 'list', 'items'],'123','1234567')
        user.facebook_id = 'an_id'
        self.assertEqual(user.facebook_id, "an_id")
        
    def test_NotfriendList(self):
        models.User.objects.create_user('user1', ['some', 'list', 'items'],'123','1234567')
        self.assertNotEqual(models.User.objects.get_user('user1').friends, ['aaaa', 'aaa', 'bbb'])
        
    def test_friendList(self):
        models.User.objects.create_user('user4', ['aaaa', 'aaa', 'bbb'],'123','1234567')
        self.assertEqual(models.User.objects.get_user('user4').friends, ['aaaa', 'aaa', 'bbb'])
        
    
    def test_subscriber(self):
        models.User.objects.create_user('team', ['some', 'list', 'items'],'133','1111111')
        models.User.objects.create_user('group', ['some', 'aaaat', 'items'],'113','13333111')
        #subscribe team with group for topic = math
        models.User.objects.subscriber('team', 'add', 'math', ['group'])
        self.assertEqual(models.User.objects.get_user('group').
                         followers.keyval_set.all()[0].key, 'team')
        self.assertEqual(models.User.objects.get_user('group').
                         followers.keyval_set.all()[0].value, 'math')
        self.assertNotEqual(models.User.objects.get_user('group').
                         followers.keyval_set.all()[0].key, 'team1')
        self.assertNotEqual(models.User.objects.get_user('group').
                         followers.keyval_set.all()[0].value, 'english')
        #unsubscribe topic math and change topic to physic
        models.User.objects.subscriber('team', 'delete', 'math', ['group'])
        models.User.objects.subscriber('team', 'add', 'physic', ['group'])
        self.assertNotEqual(models.User.objects.get_user('group').
                         followers.keyval_set.all()[0].value, 'math')
        self.assertEqual(models.User.objects.get_user('group').
                         followers.keyval_set.all()[0].value, 'physic')
        
    def test_send_message(self):
        try1 = models.User()
        try1.status = models.Status()
        try1.status.set_status('math 1', True)
        self.assertEqual(try1.notification_message('try1', 'math 1', 'math'), 
                         'user try1 posted a message about \'math\':  "math 1"')
        
    def test_send_message1(self):
        try1 = models.User()
        try1.status = models.Status()
        try1.status.set_status('math 1', True)
        self.assertNotEqual(try1.notification_message('try1', 'math 1', 'math'), 
                         'user try1 posted a message about \'math\':  "math 2"')

        
class TestLocation(unittest.TestCase):
    def test_getting_lon_lat(self):
        a = models.Location()
        a.latitude = 15.001
        a.longitude = 32.001
        self.assertEqual(15.001, a.latitude)
        self.assertEqual(32.001, a.longitude)
    
    def test_two_pt_with_same_lat_lon(self):
        pt1 = models.Location()
        pt1.latitude = 15.001
        pt1.longitude = 32.001
        pt2 = models.Location()
        pt2.latitude = 15.001
        pt2.longitude = 32.001
        self.assertEqual(pt1, pt2)
    
    def test_two_pts_with_different_lat_should_not_be_equal(self):
        pt1 = models.Location()
        pt1.latitude = 16.001
        pt1.longitude = 32.001
        pt2 = models.Location()
        pt2.latitude = 15.001
        pt2.longitude = 32.001
        self.assertNotEqual(pt1.latitude, pt2.latitude)
    
    def test_two_pts_with_different_lon_should_not_be_equal(self):
        pt1 = models.Location()
        pt1.latitude = 15.001
        pt1.longitude = 32.001
        pt2 = models.Location()
        pt2.latitude = 15.001
        pt2.longitude = 62.001
        self.assertNotEqual(pt1.longitude, pt2.longitude)
    
    def test_is_not_equal_when_comparison_is_not_Location_object(self):
        pt1 = models.Location()
        pt1.latitude = 15.001
        pt1.longitude = 32.001
        pt2 = "15.001,32.001"
        self.assertNotEqual(pt1, pt2)
    
    def test_lat_midpt_equal_both_given_pt(self):
        pt1 = models.Location()
        pt1.latitude = 15.001
        pt1.longitude = 32.001
        pt2 = models.Location()
        pt2.latitude = 15.001
        pt2.longitude = 62.001
        mid1 = pt1.midpoint(pt2)
        mid2 = pt2.midpoint(pt1)
        self.assertEqual(mid1.latitude, mid2.latitude)
    
    def test_lon_midpt_equal_both_given_pt(self):
        pt1 = models.Location()
        pt1.latitude = 15.001
        pt1.longitude = 32.001
        pt2 = models.Location()
        pt2.latitude = 15.001
        pt2.longitude = 62.001
        mid1 = pt1.midpoint(pt2)
        mid2 = pt2.midpoint(pt1)
        self.assertEqual(mid1.longitude, mid2.longitude)
    
    def test_lat_midpoint_not_equal_given_point(self):
        pt1 = models.Location()
        pt1.latitude = 15.001
        pt1.longitude = 32.001
        pt2 = models.Location()
        pt2.latitude = 15.001
        pt2.longitude = 62.001
        mid1 = pt1.midpoint(pt2)
        mid2 = pt2.midpoint(pt1)
        self.assertNotEqual(pt1.latitude, mid1.latitude)
        self.assertNotEqual(pt2.latitude, mid2.latitude)
    
    def test_lon_midpoint_not_equal_given_point(self):
        pt1 = models.Location()
        pt1.latitude = 15.001
        pt1.longitude = 32.001
        pt2 = models.Location()
        pt2.latitude = 15.001
        pt2.longitude = 62.001
        mid1 = pt1.midpoint(pt2)
        mid2 = pt2.midpoint(pt1)
        self.assertNotEqual(pt1.longitude, mid1.longitude)
        self.assertNotEqual(pt2.longitude, mid2.longitude)
    
    def test_get_msm(self):
        user1 = models.Chat()
        user1.user1id = 'user1'
        user2 = models.Chat()
        user2.user2id = 'user2'
        user1.add_message('user1', 'message from user1')
        self.assertIsNotNone(user1.messages, 'message added')
        
    def test_get_msm1(self):
        user1 = models.Chat()
        user1.user1id = 'user1'
        user2 = models.Chat()
        user2.user2id = 'user2'
        user1.add_message('user1', 'message from user1')
        user1.connected('user1')
        self.assertIsNone(user1.visited('user1'), 'user visited')
        
    def test_get_msm2(self):
        user1 = models.Chat()
        user1.user1id = 'user1'
        user2 = models.Chat()
        user2.user2id = 'user2'
        user2.add_message('user2', 'message from user2')
        user1.add_message('user1', 'message from user1')
        self.assertNotEqual(user1.get_updates('user2'), user2.get_updates('user1'))
        
    def test_meeting(self):
        data = {'userId': 'aaa', 'friendId': '123', 'userLocation': {'latitude':12, 'longitude': 14},
                 'friendLocation':{ 'latitude': 14, 'longitude':15}, 'meetingName': 'Soda Hall',
                 'meetingLocation': {'latitude': 12, 'longitude': 14}}
        meeting = models.Meeting.objects.create_meeting(data)
        self.assertEqual(meeting.friends,['aaa', '123'])
        self.assertEqual(meeting.latitude,12)
        self.assertEqual(meeting.longitude,14)
        self.assertEqual(meeting.meeting_name,'Soda Hall')
        
    def test_meeting1(self):
        data = {'userId': 'bbb', 'friendId': '123', 'userLocation': {'latitude':12, 'longitude': 14},
                 'friendLocation':{ 'latitude': 14, 'longitude':15}, 'meetingName': 'Soda Hall',
                 'meetingLocation': {'latitude': 12, 'longitude': 14}}
        meeting = models.Meeting.objects.create_meeting(data)
        self.assertNotEqual(meeting.friends,['aaa', '123'])
        self.assertNotEqual(meeting.latitude,14)
        self.assertEqual(meeting.longitude,14)
        self.assertEqual(meeting.meeting_name,'Soda Hall')
        
        
        
        
        
        
        