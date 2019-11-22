from flask import jsonify
from flask import Blueprint

from classes.Errors import NoStats, UserException, NoUser
from classes.Stats import Stats
from classes.Utils import getUser
from database import StatsTab, db
from background import calc_stats_async

stats = Blueprint('stats', __name__)


@stats.route('/stats/<user_id>', methods=['GET'])
def _reaction(user_id):
    q = db.session.query(StatsTab).filter(StatsTab.user_id == user_id)
    stats_db: StatsTab = q.first()
    calc_stats_async.delay(user_id)

    if not stats_db:
        try:
            getUser(user_id)
        except UserException:
            return NoUser

        return NoStats()

    return stats_db.to_json()

class UserNonExistsError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


