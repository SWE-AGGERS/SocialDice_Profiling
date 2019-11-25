# encoding: utf8
import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db.session.configure()


class StatsTab(db.Model):
    __tablename__ = 'stats'

    user_id = db.Column(db.Integer, primary_key=True, name='user_id')

    email = db.Column(db.String, name='email')
    firstname = db.Column(db.String, name='firstname')
    lastname = db.Column(db.String, name='lastname')

    numStories = db.Column(db.Integer, name='numStories')
    likes = db.Column(db.Integer, name='likes')
    dislikes = db.Column(db.Integer, name='dislikes')
    numDice = db.Column(db.Integer, name='numDice')

    avgLike = db.Column(db.Float, name='avgLike')
    avgDislike = db.Column(db.Float, name='avgDislike')
    avgDice = db.Column(db.Float, name='avgDice')

    ratio_likeDislike = db.Column(db.Float, name='ratio_likeDislike')
    love_level = db.Column(db.Integer, name='love_level')

    def to_json(self):
        # stats_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        self
        stats_dict = {
            "user_id": self.user_id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,

            "numStories": self.numStories,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "numDice ": self.numDice,

            "avgLike": self.avgLike,
            "avgDislike": self.avgDislike,
            "avgDice": self.avgDice,

            "ratio_likeDislike": self.ratio_likeDislike,
            "love_level": self.love_level
        }
        return json.dumps(stats_dict)
