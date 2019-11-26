import unittest
from unittest import mock
from stats_service.classes.Stats import Stats
from stats_service.classes.Stories import Stories, Story
from stats_service.classes.User import User
from stats_service.classes.Utils import ENDPOINT_USER, ENDPOINT_STORIES
from stats_service.tests.common_tests_utility import mocked_get_ok, user1_json, story_block1_json


class StatsTestCase(unittest.TestCase):
    def test_Response_User(self):

        res = mocked_get_ok(url=ENDPOINT_USER)

        self.assertEqual(200, res.status_code, 'Wrong status code: 200 !='+str(res.status_code))

        usr: User = User(res.data)
        self.assertEqual(user1_json['id'], usr.id)
        self.assertEqual(user1_json['email'], usr.email)
        self.assertEqual(user1_json['firstname'], usr.firstname)
        self.assertEqual(user1_json['lastname'], usr.lastname)

    def test_Response_Stories(self):

        res = mocked_get_ok(url=ENDPOINT_STORIES)

        self.assertEqual(200, res.status_code, 'Wrong status code: 200 !='+str(res.status_code))

        stories: Stories = Stories(res.data)
        i = 0
        for s in stories.storylist:
            s: Story
            s_dict = story_block1_json['stories'][i]
            self.assertEqual(s_dict['id'],s.id)
            self.assertEqual(s_dict['text'], s.text)
            self.assertEqual(s_dict['roll'], s.roll)
            self.assertEqual(s_dict['dicenumber'], s.dicenumber)
            self.assertEqual(s_dict['likes'], s.likes)
            self.assertEqual(s_dict['dislikes'], s.dislikes)
            self.assertEqual(s_dict['author_id'], s.author_id)
            self.assertEqual(s_dict['date'], s.date)
            i += 1

    @mock.patch('requests.get', side_effect=mocked_get_ok)
    def test_Stats(self, mock_g):
        stat = Stats(1)

        self.assertEqual(user1_json['id'], stat.user.id)
        self.assertEqual(user1_json['email'], stat.user.email)
        self.assertEqual(user1_json['firstname'], stat.user.firstname)
        self.assertEqual(user1_json['lastname'], stat.user.lastname)
        self.assertEqual(6.0, stat.avgDice)
        self.assertEqual(85.0, stat.avgDislike)
        self.assertEqual(197.33, stat.avgLike)
        self.assertEqual(255, stat.dislikes)
        self.assertEqual(592, stat.likes)
        self.assertEqual(337, stat.love_level)
        self.assertEqual(18, stat.numDice)
        self.assertEqual(3, stat.numStories)
        self.assertEqual(2.32, stat.ratio_likeDislike)


if __name__ == '__main__':
    unittest.main()
