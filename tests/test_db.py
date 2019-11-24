from sqlalchemy.orm import scoped_session
from app import create_app
import unittest
import mock
from background import calc_stats_async
from database import db, StatsTab
from tests.common_tests_utility import mocked_get_ok, user1_json


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
            db.drop_all()
            db.create_all()

            calc_stats_async(user1_json['id'])

            session = db.session

            stats_check: StatsTab = session.query(StatsTab).filter(StatsTab.user_id == user1_json['id']).first()
            self.assertIsNotNone(stats_check)
            self.assertEqual(user1_json['id'], stats_check.user_id)
            self.assertEqual(user1_json['email'], stats_check.email)

    @mock.patch('requests.get', side_effect=mocked_get_ok)
    def test_Update_Async(self, pippo):
        _app = create_app(debug=True)
        with _app.app_context():
            db.drop_all()
            db.create_all()

            # task = calc_stats_async
            # delay: AsyncResult = task.delay(user_id=user1_json['id'])
            # get = delay.get(timeout=10)

            calc_stats_async.delay(user_id=user1_json['id']).get(timeout=5)

            # sleep(10.0)

            session = db.session
            stats_check: StatsTab = session.query(StatsTab).filter(StatsTab.user_id == user1_json['id']).first()
            self.assertIsNotNone(stats_check)
            self.assertEqual(user1_json['id'], stats_check.user_id)
            self.assertEqual(user1_json['email'], stats_check.email)
