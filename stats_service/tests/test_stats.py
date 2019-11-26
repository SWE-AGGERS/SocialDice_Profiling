import json
import unittest
from unittest import mock

from stats_service.app import create_app
from classes.Errors import NoStats
from stats_service.database import db
from tests.common_tests_utility import mocked_get_ok, user1_json, mocked_background_delay_ok, \
    mocked_background_delay_No_update


class GlobalTestCase(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mocked_get_ok)
    @mock.patch('background.calc_stats_async.delay', side_effect=mocked_background_delay_ok)
    def test_getstats(self, pippo, pluto):
        _app = create_app(debug=True)
        with _app.app_context():
            app = _app.test_client()
            db.drop_all()
            db.create_all()

            # calc_stats_async(user1_json['id'])

            # reply = _get_stats(user1_json['id'])
            # print(reply)
            reply = app.get('/stats/' + str(user1_json['id']))
            body = json.loads(str(reply.data, 'utf8'))

            self.assertEqual(user1_json['id'], body['user_id'])
            self.assertEqual(user1_json['email'], body['email'])
            # session = db.session
            #
            # stats_check: StatsTab = session.query(StatsTab).filter(StatsTab.user_id == user1_json['id']).first()
            # self.assertIsNotNone(stats_check)
            # self.assertEqual(user1_json['id'], stats_check.user_id)
            # self.assertEqual(user1_json['email'], stats_check.email)

    @mock.patch('requests.get', side_effect=mocked_get_ok)
    @mock.patch('background.calc_stats_async.delay', side_effect=mocked_background_delay_No_update)
    def test_getstats_fail(self, pippo, pluto):
        _app = create_app(debug=True)
        with _app.app_context():
            app = _app.test_client()
            db.drop_all()
            db.create_all()

            reply = app.get('/stats/' + str(user1_json['id']))
            body = json.loads(str(reply.data, 'utf8'))

            expected = NoStats()
            self.assertEqual(expected['code'], body['code'])
            self.assertEqual(expected['data'], body['data'])


if __name__ == '__main__':
    unittest.main()
