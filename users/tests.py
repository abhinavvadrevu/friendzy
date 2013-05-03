"""
    This file demonstrates writing tests using the unittest module. These will pass
    when you run "manage.py test".
    
    Replace this with more appropriate tests for your application.
    """
import sys, os
sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path
import unittest
import datetime as dt
from users import models


class UserTest(unittest.TestCase):
    
    #@patch('models.User.get_friend_statuses')
    def test_user_exists(self):
        # objects.create creates and saves a db entry in one step
        models.User.objects.create_user('an_id', ['some', 'list', 'items'],'123', '1234567')
        self.assertTrue(models.User.objects.user_exists('an_id'),"user_exists test fails")
    
    def test_user_reset(self):
        # objects.create creates and saves a db entry in one step
        models.User.objects.create_user('an_id', ['some', 'list', 'items'],'123', '1234567')
        self.assertTrue(models.User.objects.user_exists('an_id'),"user_exists test fails")
        models.User.TESTAPI_resetFixture()
        self.assertFalse(models.User.objects.user_exists('an_id'),"user_reset test fails")
    
    def test_user_exists1(self):
        # objects.create creates and saves a db entry in one step
        models.User.objects.create_user('user1', ['some', 'list', 'items'],'123', '1234567')
        self.assertTrue(models.User.objects.user_exists('user1'),"user exits")
    
    def test_user_exists2(self):
        # objects.create creates and saves a db entry in one step
        models.User.objects.create_user('user1', ['some', 'list', 'items'],'123', '1234567')
        self.assertFalse(models.User.objects.user_exists('user2'),"user does not exit")
    
    def test_user_exits3(self):
        user = models.User.objects.create_user('an_id', ['some', 'list', 'items'], '1234', '12345678')
        self.assertEqual(user.facebook_id, 'an_id')
        self.assertEqual(user.phone_number, '12345678')
        self.assertEqual(user.friends, ['some', 'list', 'items'])
        self.assertEqual(user.regId, '1234')
    
    def test_user_exits4(self):
        user = models.User.objects.create_user('an_id', ['some', 'list', 'items'], '1234', '12345678')
        self.assertNotEqual(user.facebook_id, 'another_id')
        self.assertEqual(user.phone_number, '12345678')
        self.assertNotEqual(user.friends, ['some', 'other', 'items'])
        self.assertEqual(user.regId, '1234')
    
    def test_user_exits5(self):
        models.User.objects.create_user('user_test1', ['one', 'two', 'tree'], 'a1234', '123469294')
        sample_model = models.User.objects.get_user('user_test1')
        self.assertEqual(sample_model.friends, ['one', 'two', 'tree'])
        self.assertEqual(sample_model.facebook_id,'user_test1')
        self.assertEqual(sample_model.phone_number, '123469294')
        self.assertEqual(sample_model.regId,'a1234')
    
    
    def test_user_exits6(self):
        trying1 = models.User.objects.create_user('user_test2', ['some', 'aaa', 'items'],'193', '357943')
        self.assertEqual(trying1.login( ['some', 'aaa', 'items'], '193'), {'data': {}})
    
    def test_user_exit7(self):
        trying1 = models.User.objects.create_user('an_id', ['some'],'123', '1234567')
        trying2 = models.User.objects.create_user('some', ['an_id'],'195', '357943')
        self.assertEqual(trying1.friends[0], trying2.facebook_id)
        self.assertEqual(trying2.friends[0], trying1.facebook_id)
    
    def test_user_exists8(self):
        a = models.UserManager()
        self.assertFalse(a.user_exists('1'), 'user has not created yet')
    
    def test_user_exists9(self):
        models.User.objects.create_user('yyy', ['some'],'123', '1234567')
        app = models.Appeal()
        self.assertEqual(app.get_regId('yyy'), '123')
        app.uid = 'new'
        app.friendid = 'old'
        app.latitude = 37.879719
        app.longitude = -122.260744
        a = app.get_data('old', 37.879719,-122.260744)
        self.assertEqual(a['userLocation'],{'latitude': 37.879719, 'longitude': -122.260744})
        self.assertEqual(a['suggested_meetups'][0],
                         {'meetingLocation': {'latitude': 37.8795938, 'longitude': -122.2689348},
                         'meetingName': 'Chez Panisse'})
    
    def test_user_exists10(self):
        models.User.objects.create_user('hongle1', ['anh1'],'30091', '77777')
        models.User.objects.create_user('anh1', ['hongle1'],'26091', '66666')
        self.assertEqual(models.Appeal.objects.notify('hongle1','anh1'), None)
        self.assertFalse(models.Appeal.objects.appeal_exists('hongle1','anh1'), 'exists')
    
    
    def test_appeal(self):
        models.User.objects.create_user('user_a', ['some', 'list', 'items'],'123', '1234567')
        models.User.objects.create_user('user_b', ['someaa', 'rrrr', 'items'],'333', '523253523')
        self.assertIsNone(models.Appeal.objects.create_appeal('user_a', 'user_b', 1234, 2345),
                          'create appeal test failed')
        self.assertTrue(models.Appeal.objects.appeal_exists('user_a', 'user_b'), 'appeal does not exists')
        self.assertIsNone(models.Appeal.objects.notify('user_a', 'user_b'),'appeal notify test failed')
        a = models.Appeal.objects.get_appeal('user_a', 'user_b')
        self.assertEqual(a.latitude, 1234.0)
        self.assertEqual(a.longitude, 2345.0)
        self.assertEqual(a.uid, 'user_a')
        self.assertEqual(a.friendid, 'user_b')
    
    def test_appeal1(self):
        models.Appeal.objects.create_appeal('user_a', 'user_b', 1234, 2345)
        a = models.Appeal()
        a.uid = 'user_a'
        a.friendid = 'user_b'
        a.latitude = 37.879719
        a.longitude = -122.260744
        self.assertEqual(a.get_data('user_b', 37.879719, -122.260744), {'userLocation': {'latitude': 37.879719,
                         'longitude': -122.260744}, 'suggested_meetups': [{'meetingLocation': {'latitude': 37.8795938,
                                                                          'longitude': -122.2689348}, 'meetingName': u'Chez Panisse'}, {'meetingLocation': {'latitude': 37.8754053,
                                                                          'longitude': -122.2600086}, 'meetingName': u"Celia's"}, {'meetingLocation': {'latitude': 37.8795938,
                                                                          'longitude': -122.2689348}, 'meetingName': u'Chez Panisse Cafe'}, {'meetingLocation': {'latitude': 37.8758265,
                                                                          'longitude': -122.2602064}, 'meetingName': u'Jasmine Thai'}, {'meetingLocation': {'latitude': 37.8770724,
                                                                          'longitude': -122.2691332}, 'meetingName': u'Da Lian'}], 'friendLocation': {'latitude': 37.879719,
                         'longitude': -122.260744}, 'userId': 'user_a', 'friendId': 'user_b'})
    
    def test_Status(self):
        status1 = models.Status()
        ans = "ABC"
        status1.set_status(ans,True)
        self.assertEqual(status1.status, ans)
    
    def test_Status2(self):
        status1 = models.Status()
        ans = "ABC"
        wrong = '123'
        status1.set_status(ans,True)
        self.assertNotEqual(status1.status, wrong)
    
    def test_Status3(self):
        status1 = models.Status()
        ans = "ABC"
        status1.set_status(ans,True)
        self.assertEqual(status1.get_status(), ans)
    
    def test_Status4(self):
        trying1 = models.User.objects.create_user('an_id', ['some'],'123', '1234567')
        self.assertEqual(trying1.get_friend_statuses(), {})
    
    def test_statu5(self):
        a = models.Status.objects.create_status()
        self.assertEqual(a.status, '')
        a.status = 'status'
        self.assertEqual(a.status, 'status')
    
    
    def test_chat1(self):
        models.Chat.objects.create_chat('userID', 'friendID')
        self.assertTrue(models.Chat.objects.chat_exists('userID', 'friendID'), ' chat not exists')
    
    def test_chat2(self):
        models.Chat.objects.create_chat('userID', 'friendID')
        self.assertFalse(models.Chat.objects.chat_exists('userID1', 'friendID'), 'chat fail: wrong user ID')
    
    def test_chat3(self):
        models.Chat.objects.create_chat('userID', 'friendID')
        self.assertFalse(models.Chat.objects.chat_exists('userID', 'friendID1'), 'chat fail: wrong friend ID')
    
    def test_chat4(self):
        a =  models.Chat.objects.create_chat('userID', 'friendID')
        self.assertEqual(a.user1id, 'userID')
        self.assertEqual(a.user2id, 'friendID')
        a.add_message('userID', 'how are you?')
        self.assertEqual(a.messages[0][0], 'how are you?')
    
    def test_chat5(self):
        b = models.Chat.objects.create_chat('hong', 'anh')
        b.add_message('anh', 'chat')
        bb = models.Chat.objects.get_chat('hong','anh')
        self.assertEqual(bb.messages[0][0], 'chat')
        self.assertEqual(bb.messages[0][2], 'anh')
    
    
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
    
    def test_status_from_user2(self):
        a = models.User.objects.create_user('user1', ['some', 'list', 'items'],'123','1234567')
        self.assertEqual(a.set_status('hi',True), {'data': {}})
        self.assertEqual(a.get_status(), 'hi')
    
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
    
    def test_set_location(self):
        pt1 = models.Location()
        pt1.set_location(12,13)
        self.assertEqual(pt1.latitude, 12)
        self.assertEqual(pt1.longitude, 13)
    
    def test_get_midpoint_method(self):
        pt1 = models.Location()
        pt1.set_location(12,13)
        pt2 = models.Location()
        pt2.set_location(14,15)
        midpoint11 = pt1.midpoint(pt2)
        self.assertEqual(midpoint11.latitude, 13.001912951949645)
        self.assertEqual(midpoint11.longitude, 13.995969771506447)
    
    def test_get_meeting_location(self):
        pt1 = models.Location()
        pt1.set_location(37.879719,-122.260744)
        pt2 = models.Location()
        pt2.set_location(42.752,-122.489)
        a = pt1.get_meeting_point(pt2)
        self.assertEqual(a[0]['latitude'], 40.3849469)
        self.assertEqual(a[0]['longitude'], -122.2815379)
        self.assertEqual(a[0]['name'], 'Main Street Diner')
        self.assertEqual(a[0]['address'], '3342 Main St Cottonwood, CA 96022')
        self.assertEqual(a[1]['latitude'], 40.388498)
        self.assertEqual(a[1]['longitude'], -122.288442)
        self.assertEqual(a[1]['name'], "Eagle's Nest Pizza")
        self.assertEqual(a[1]['address'], '20633 Gas Point Rd Ste D Cottonwood, CA 96022')
    
    
    def test_get_distance_method(self):
        pt1 = models.Location()
        pt1.set_location(37.879719,-122.260744)
        pt2 = models.Location()
        pt2.set_location(42.752,-122.489)
        self.assertEqual(pt1.get_distance(pt2), 541.7774423815335)
    
    def test_gmc(self):
        data77 = {'userId': 'qqq', 'friendId': '09483', 'userLocation': {'latitude':37.879719, 'longitude': -122.260744},
            'friendLocation':{ 'latitude': 42.752, 'longitude':-122.489}, 'meetingName': 'Soda Hall',
            'meetingLocation': {'latitude': 40.3849469, 'longitude': -122.2815379}}
        models.User.objects.create_user('team', ['some', 'list', 'items'],'133','1111111')
    
    
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
    
    def test_add_msm_and_update(self):
        chating1 = models.Chat()
        chating1.user1id = 'user22'
        chating1.user2id = 'user33'
        chating1.add_message('user22', 'hi')
        self.assertEqual(chating1.messages[0][0], 'hi')
        self.assertEqual(chating1.messages[0][2], 'user22')
        a = chating1.get_updates('user33')
        self.assertEqual(a[0][0], 'hi')
        self.assertIsNone(chating1.visited('user22'), 'user have not visited')
        today = dt.date.today()
        self.assertEqual(chating1.user1lastvisit.year, today.year)
        self.assertEqual(chating1.user1lastvisit.month,today.month)
        self.assertEqual(chating1.user1lastvisit.day,today.day)
        self.assertTrue(chating1.connected('user22'), 'user not connected')
        self.assertFalse(chating1.connected('user33'), 'user connected')
    
    def test_sms(self):
        models.User.objects.create_user('group00', ['some', 'aaaat', 'items'],'113','13333111')
        models.User.objects.create_user('team00', ['some', 'list', 'items'],'133','1111111')
        models.User.objects.subscriber('team00', 'add', 'test', ['group00'])
        a = models.User.objects.get_user('group00')
        a.send_sms('hello')
        a.setsms(13333111)
        self.assertTrue(a.sms, 'sms set')
        notify = a.notifyfollowers('test')
        self.assertIsNone(notify, 'sent')
        self.assertEqual(a.followers.keyval_set.all()[0].value, 'test')
        self.assertEqual(a.followers.keyval_set.all()[0].key, 'team00')
        b = a.appendkv('team00', 'math')
        self.assertIsNone(b, 'subscribe')
        self.assertEqual(a.followers.keyval_set.all()[1].value, 'math')
        self.assertEqual(a.followers.keyval_set.all()[1].key, 'team00')
    
    def test_meeting(self):
        data = {'userId': 'bbb', 'friendId': '123',
            'suggested_meetups': [{'meetingName': 'Soda Hall',
                                  'meetingLocation': { 'latitude': 344, 'longitude': 433 }},] # end of suggested_meetups
            }#end of data
        
        meeting = models.Meeting.objects.create_meeting(data)
        self.assertEqual(meeting.friends,['bbb', '123'])
        self.assertEqual(meeting.latitude,344)
        self.assertEqual(meeting.longitude,433)
        self.assertEqual(meeting.meeting_name,'Soda Hall')
    
    def test_meeting1(self):
        data = {'userId': 'bbb', 'friendId': '123',
            'suggested_meetups': [{'meetingName': 'Soda Hall',
                                  'meetingLocation': { 'latitude': 344, 'longitude': 433 }},] # end of suggested_meetups
            }#end of data
        
        meeting = models.Meeting.objects.create_meeting(data)
        self.assertNotEqual(meeting.friends,['aaa', '123'])
        self.assertNotEqual(meeting.latitude,222)
        self.assertEqual(meeting.longitude,433)
        self.assertEqual(meeting.meeting_name,'Soda Hall')
    
    def test_meeting2(self):
        data = {'userId': 'bbb', 'friendId': '123',
            'suggested_meetups': [{'meetingName': 'Soda Hall',
                                  'meetingLocation': { 'latitude': 344, 'longitude': 433 }},] # end of suggested_meetups
            }#end of data
        a1 = models.Meeting.objects.create_meeting(data)
        self.assertEqual(models.Meeting.objects.get_meetings(12,13), {'data': []})
    
    
    def test_meeting3(self):
        testm = models.Meeting()
        self.assertEqual(testm.get_data()['longitude'], 0)
        self.assertEqual(testm.get_data()['location_name'], '')
        self.assertEqual(testm.get_data()['latitude'], 0)
        self.assertEqual(testm.get_data()['attendees'], [])
    
    def test_meeting4(self):
        data = {'userId': 'bbb', 'friendId': '123',
            'suggested_meetups': [{'meetingName': 'Soda Hall',
                                  'meetingLocation': { 'latitude': 344, 'longitude': 433 }},] # end of suggested_meetups
            }#end of data
        meeting = models.Meeting.objects.create_meeting(data)
        self.assertEqual(meeting.meeting_name,'Soda Hall')
        meeting.update_location({'meetingName': 'Cory Hall', 'meetingLocation': { 'latitude': 555, 'longitude': 333 }})
        self.assertEqual(meeting.latitude,555)
        self.assertEqual(meeting.longitude,333)
        self.assertEqual(meeting.meeting_name,'Cory Hall')
    
    def test_meeting5(self):
        data = {'userId': 'bbb', 'friendId': '123',
            'suggested_meetups': [{'meetingName': 'Soda Hall',
                                  'meetingLocation': { 'latitude': 344, 'longitude': 433 }},]
            }#end of data
        models.Meeting.objects.create_meeting(data)
        self.assertEqual(models.Meeting.objects.get_meeting('bbb', '123'), False)
    
    def test_gcm(self):
        reg_ids = ['12', '145', '56']
        data = {
            'param1': '1',
            'param2': '2'
        }
        self.assertEqual(models.gcmNotification(data, reg_ids), {'worked': '1'})


#     def test_meeting6(self):
#         models.User.objects.create_user('user_a', ['some', 'list', 'items'],'123', '1234567')
#         models.User.objects.create_user('user_b', ['someaa', 'rrrr', 'items'],'333', '523253523')
#         data_test = {'userId': 'user_a', 'friendId': 'user_b',
#                 'suggested_meetups': [{'meetingName': 'Soda Hall',
#                                        'meetingLocation': { 'latitude': 344, 'longitude': 433 }},]
#                 }#end of data
#         meeting = models.Meeting.objects.create_meeting(data_test)
#         data_update = {'suggested_meetups': [{'meetingLocation': {'latitude': 555, 'longitude': 777},'meetingName': 'Cory Hall'}]}
#         models.Meeting.objects.update_meetup('user_a','user_b', data_update['suggested_meetups'][0])
#         self.assertEqual(meeting.meeting_name, 'Cory Hall')
# 
