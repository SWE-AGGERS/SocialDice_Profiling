from flask import Blueprint
from classes.Errors import NoStats, UserException, NoUser
from classes.Utils import getUser
from database import StatsTab, db
from background import calc_stats_async

stats = Blueprint('stats', __name__)


@stats.route('/stats/<user_id>', methods=['GET'])
def _get_stats(user_id):
    print('Get in local db,user`s stats with id ' + str(user_id))

    calc_stats_async.delay(user_id)
    # calc_stats_async(user_id)

    q = db.session.query(StatsTab).filter(StatsTab.user_id == user_id)
    stats_db: StatsTab = q.first()

    if not stats_db:
        try:
            getUser(user_id)
        except UserException:
            return NoUser

        return NoStats()

    ret = stats_db
    return stats_db.to_json()



