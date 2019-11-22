import json
import unittest
from unittest import mock

from requests import Response

from classes.User import User
from classes.Utils import ENDPOINT_USER


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

def mocked_get(url: str):
    if(url == ENDPOINT_USER):
        u = {
            "id": 123456,
            "email": "email@email.it",
            "firstname": "Mario",
            "lastname": "Rossi"
        }
        jpayload = json.dumps(u).encode('utf8')

        res = Response()
        res.status_code = 200
        res.data = jpayload

        return res


class StatsTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
