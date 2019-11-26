from celery import Celery

from stats_service.classes.Errors import UserException, ServiceUnreachable
from stats_service.database import db, StatsTab

from stats_service.classes.Stats import Stats

BACKEND = BROKER = 'redis://localhost:6380'
# BACKEND = BROKER = 'redis://0.0.0.0:6380'

celery = Celery(__name__, backend=BACKEND, broker=BROKER)

_APP = None


@celery.task
def calc_stats_async(user_id):
    global _APP
    if _APP is None:
        from stats_service.app import create_app
        app = create_app()
    else:
        app = _APP
    with app.app_context():
        stats: Stats

        try:
            stats = Stats(user_id)
        except UserException:
            print('Try get Stats from unknown user wit id ' + str(user_id))
            return
        except ServiceUnreachable as e:
            print(e)
            return
        except Exception as e:
            print('Unexpected Exception')
            print(e)
            return

        session = db.session

        q = session.query(StatsTab).filter(StatsTab.user_id == user_id)
        stats_db = q.first()

        if not stats_db:
            stats_db = StatsTab()
            stats_db.user_id = stats.user.id
            stats_db.email = stats.user.email
            stats_db.firstname = stats.user.firstname
            stats_db.lastname = stats.user.lastname
            session.add(stats_db)

        stats_db.numStories = stats.numStories
        stats_db.numDice = stats.numDice
        stats_db.likes = stats.likes
        stats_db.dislikes = stats.dislikes

        stats_db.avgLike = stats.avgLike
        stats_db.avgDislike = stats.avgDislike
        stats_db.avgDice = stats.avgDice

        stats_db.ratio_likeDislike = stats.ratio_likeDislike
        stats_db.love_level = stats.love_level

        # db.session.add(stats_db)
        session.commit()
