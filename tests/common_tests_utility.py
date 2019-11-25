import json
from time import sleep

from requests import Response

from background import calc_stats_async
from classes.Utils import ENDPOINT_USER, ENDPOINT_STORIES


def mocked_get_ok(*args, **kwargs):
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


def mocked_background_delay_ok(*args, **kwargs):
    if len(args) > 0:
        _id = args[0]
    else:
        _id = kwargs['uesr_id']
    calc_stats_async(_id)
    sleep(5)
    print()


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