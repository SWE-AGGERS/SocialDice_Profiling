import json
import unittest
from unittest import mock

from requests import Response

from classes.Stats import Stats
from classes.Stories import Stories, Story
from classes.User import User
from classes.Utils import ENDPOINT_USER, ENDPOINT_STORIES

user1_json = {
            "id": 123456,
            "email": "email@email.it",
            "firstname": "Mario",
            "lastname": "Rossi"
        }

story_block1_json = {
    "stories": [
        {
            "id": 1,
            "text": "asdf ghjkl qw e rty uio plmn bvcxz alo!?",
            "dicenumber": 6,
            "roll": "[face1, face2, face3, face4, face5, face6]",
            "date": '2011-11-11',
            "likes": 42,
            "dislikes": 21,
            "author_id": 1
        },
{
            "id": 2,
            "text": "asdf ghjkl qw e rty uio plmn bvcxz alo!?",
            "dicenumber": 6,
            "roll": "[face1, face2, face3, face4, face5, face6]",
            "date": '2011-11-11',
            "likes": 130,
            "dislikes": 24,
            "author_id": 1
        },
{
            "id": 3,
            "text": "asdf ghjkl qw e rty uio plmn bvcxz alo!?",
            "dicenumber": 6,
            "roll": "[face1, face2, face3, face4, face5, face6]",
            "date": '2011-11-11',
            "likes": 420,
            "dislikes": 210,
            "author_id": 1
        }
    ]
}


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://someurl.com/test.json':
        return MockResponse({"key1": "value1"}, 200)
    elif args[0] == 'http://someotherurl.com/anothertest.json':
        return MockResponse({"key2": "value2"}, 200)

    return MockResponse(None, 404)


def mocked_get(*args, **kwargs):
    if len(args) > 0:
        url = args[0]
    else:
        url = kwargs['url']

    if url.find(ENDPOINT_USER) != -1:
        jpayload = json.dumps(user1_json).encode('utf8')
    elif url.find(ENDPOINT_STORIES) != -1:
        jpayload = json.dumps(story_block1_json).encode('utf8')
    else:
        raise Exception('endpoint unknown: ne user, ne story: ' + url)

    res = Response()
    res.status_code = 200
    res.data = jpayload

    return res


class StatsTestCase(unittest.TestCase):
    def test_Response_User(self):

        res = mocked_get(url=ENDPOINT_USER)

        self.assertEqual(200, res.status_code, 'Wrong status code: 200 !='+str(res.status_code))

        usr: User = User(res.data)
        self.assertEqual(user1_json['id'], usr.id)
        self.assertEqual(user1_json['email'], usr.email)
        self.assertEqual(user1_json['firstname'], usr.firstname)
        self.assertEqual(user1_json['lastname'], usr.lastname)

    def test_Response_Stories(self):

        res = mocked_get(url=ENDPOINT_STORIES)

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

    @mock.patch('requests.get', side_effect=mocked_get)
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
