import json
from time import sleep

from requests import Response
from sqlalchemy.orm import scoped_session

from app import create_app

import unittest
import mock


# class TestReactionDB(unittest.TestCase):
#
#     def test1(self):
#         _app = create_app(debug=True)
#
#         with mock.patch('service.views.reactions.exist_story') as exist_story_mock:
#             exist_story_mock.return_value = True
#             with _app.app_context():
from background import calc_stats_async
from classes.Utils import ENDPOINT_USER, ENDPOINT_STORIES
from database import db, StatsTab

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

class TestStatsDB(unittest.TestCase):

    def test_initDB(self):
        _app = create_app(debug=True)
        with _app.app_context():
            db.drop_all()
            db.create_all()

            session: scoped_session = db.session

            stats_record1: StatsTab = StatsTab()

            stats_record1.user_id = 30
            stats_record1.email = 'email@email.com'
            stats_record1.firstname = 'Mario'
            stats_record1.lastname = 'Rossi'

            session.add(stats_record1)
            session.commit()

            stats_check: StatsTab = session.query(StatsTab).filter(StatsTab.user_id == 30).first()
            self.assertIsNotNone(stats_check)
            self.assertEqual(stats_record1.user_id, stats_check.user_id)
            self.assertEqual(stats_record1.email, stats_check.email)

            stats_check.email = 'modified.email@email.ru'
            session.commit()

            stats_check_mod: StatsTab = session.query(StatsTab).filter(StatsTab.user_id == 30).first()
            self.assertIsNotNone(stats_check_mod)
            self.assertNotEqual('email@email.com', stats_check_mod.email)

    @mock.patch('requests.get', side_effect=mocked_get_ok)
    def test_Update(self, pippo):
        _app = create_app(debug=True)
        with _app.app_context():
            calc_stats_async(user1_json['id'])

            session = db.session
            stats_check: StatsTab = session.query(StatsTab).filter(StatsTab.user_id == user1_json['id']).first()
            self.assertIsNotNone(stats_check)
            self.assertEqual(user1_json['id'], stats_check.user_id)
            self.assertEqual(user1_json['email'], stats_check.email)


    # def test0(self):
    #     global _app
    #     if _app is None:
    #         tested_app = create_app(debug=True)
    #         _app = tested_app
    #     # db.drop_all()
    #     # db.create_all()
    #     # create reaction
    #     with mock.patch('reactions_service.views.reactions.exist_story') as exist_story_mock:
    #         exist_story_mock.return_value = True
    #         res = add_reaction(1, 1, 1)
    #         print(res)




    #
    #
    # def test1(self):
    #     global _app
    #     tested_app = create_app(debug=True)
    #     _app = tested_app
    #
    #     with tested_app.test_client() as client:
    #         init_db_testing(client)
    #         # create like to story 1 from user 1
    #         reply = client.post('/stories/reaction/1/1/1')
    #         body = json.loads(str(reply.data, 'utf8'))
    #         self.assertEqual(body['reaction'], '1')
    #         self.assertEqual(body['reply'], 'Reaction created!')
    #         self.assertEqual(body['story_id'], '1')
    #
    #         # remove like
    #         reply = client.post('/stories/reaction/1/1/1')
    #         body = json.loads(str(reply.data, 'utf8'))
    #         self.assertEqual(body['reaction'], '1')
    #         self.assertEqual(body['reply'], 'Reaction removed!')
    #         self.assertEqual(body['story_id'], '1')
    #
    #         # create dislike
    #         reply = client.post('/stories/reaction/1/2/1')
    #         body = json.loads(str(reply.data, 'utf8'))
    #         self.assertEqual(body['reaction'], '2')
    #         self.assertEqual(body['reply'], 'Reaction created!')
    #         self.assertEqual(body['story_id'], '1')
    #
    #         # change reaction dislike -> like
    #         reply = client.post('/stories/reaction/1/1/1')
    #         body = json.loads(str(reply.data, 'utf8'))
    #         self.assertEqual(body['reaction'], '1')
    #         self.assertEqual(body['reply'], 'Reaction changed!')
    #         self.assertEqual(body['story_id'], '1')
    #
    #         # create dislike
    #         reply = client.post('/stories/reaction/2/2/1')
    #         body = json.loads(str(reply.data, 'utf8'))
    #         self.assertEqual(body['reaction'], '2')
    #         self.assertEqual(body['reply'], 'Reaction created!')
    #         self.assertEqual(body['story_id'], '2')
    #
    #         #
    #         #
    #         # self.assertEqual(body, "{'reaction': '1', 'reply': 'Reaction removed!', 'story_id': '1'}")
    #
    # def test2(self):
    #     global _app
    #     tested_app = create_app(debug=True)
    #     _app = tested_app
    #
    #     with tested_app.test_client() as client:
    #         init_db_testing(client)
    #
    #         for ii in range(1, 101):
    #             # create like to story 1 from user 1
    #             reply = client.post('/stories/reaction/1/1/' + str(ii))
    #             body = json.loads(str(reply.data, 'utf8'))
    #             self.assertEqual(body['reaction'], '1')
    #             self.assertEqual(body['reply'], 'Reaction created!')
    #             self.assertEqual(body['story_id'], '1')
    #
    #         for ii in range(101, 201):
    #             # create like to story 1 from user 1
    #             reply = client.post('/stories/reaction/1/2/' + str(ii))
    #             body = json.loads(str(reply.data, 'utf8'))
    #             self.assertEqual(body['reaction'], '2')
    #             self.assertEqual(body['reply'], 'Reaction created!')
    #             self.assertEqual(body['story_id'], '1')
    #
    #         # get number of like (100)
    #         # get number of dislike (100)

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
