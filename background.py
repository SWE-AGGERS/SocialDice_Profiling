from celery import Celery
from sqlalchemy.orm import scoped_session

from database import db, StatsTab
from sqlalchemy import and_

from classes.Stats import Stats

BACKEND = BROKER = 'redis://localhost:6379'
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

_APP = None


@celery.task
def calc_stats_async(user_id):
    global _APP
    if _APP is None:
        from app import create_app
        app = create_app()
    else:
        app = _APP
    with app.app_context():
        Stats(user_id)

        q = db.session.query(StatsTab).filter(StatsTab.user_id == user_id)
        stats_db = q.first()

        if not stats_db:
            stats_db = StatsTab()
            stats_db.user_id = Stats.user.id
            stats_db.email = Stats.user.email
            stats_db.firstname = Stats.user.firstname
            stats_db.lastname = Stats.user.lastname
            # db.session.add(stats_db)

        stats_db.numStories = Stats.numStories
        stats_db.numDice = Stats.numDice
        stats_db.likes = Stats.likes
        stats_db.dislikes = Stats.dislikes

        stats_db.avgLike = Stats.avgLike
        stats_db.avgDislike = Stats.avgDislike
        stats_db.avgDice = Stats.avgDice

        stats_db.ratio_likeDislike = Stats.ratio_likeDislike
        stats_db.love_level = Stats.love_level

        # db.session.add(stats_db)
        # db.session.commit()
        stats_db.save()
