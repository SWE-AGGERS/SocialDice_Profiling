# encoding: utf8
import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class StatsTab(db.Model):
    __tablename__ = 'stats'

    user_id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)

    numStories = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    numDice = db.Column(db.Integer)

    avgLike = db.Column(db.Float)
    avgDislike = db.Column(db.Float)
    avgDice = db.Column(db.Float)

    ratio_likeDislike = db.Column(db.Float)
    love_level = db.Column(db.Integer)

    def to_json(self):
        stats_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return json.dumps(stats_dict)
