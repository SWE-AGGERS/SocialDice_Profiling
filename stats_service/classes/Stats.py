from classes.Stories import Stories, Story
from classes.User import User
from classes.Utils import getUser, getStories


class Stats(dict):
    user: User

    numStories: int
    likes: int
    dislikes: int
    numDice: int

    avgLike: float
    avgDislike: float
    avgDice: float

    ratio_likeDislike: float
    love_level: int

    def __init__(self, id: int):
        super().__init__()

        self.user = getUser(id)

        stories: Stories = getStories(id)

        self.numStories = len(stories.storylist)
        if not self.numStories:
            self.numStories = 0

        self.likes = 0
        self.dislikes = 0
        self.numDice = 0

        for s in stories.storylist:
            s: Story
            self.likes += s.likes
            self.dislikes += s.dislikes
            self.numDice += s.dicenumber

        if self.numStories != 0:
            self.avgLike = round(self.likes/self.numStories, 2)
            self.avgDislike = round(self.dislikes / self.numStories, 2)
            self.avgDice = round(self.numDice / self.numStories, 2)
        else:
            self.avgLike = 0
            self.avgDislike = 0
            self.avgDice = 0

        if self.dislikes != 0:
            self.ratio_likeDislike = round(self.likes / self.dislikes,2)
        else:
            self.ratio_likeDislike = 0

        self.love_level = self.likes - self.dislikes

    def jsonify(self):
        self['user'] = self.user.jsonify()

        self['numStories'] = self.numStories
        self['likes'] = self.likes
        self['dislikes'] = self.dislikes
        self['numDice'] = self.numDice

        self['avgLike'] = self.avgLike
        self['avgDislike'] = self.avgDislike
        self['avgDice'] = self.avgDice

        self['ratio_likeDislike'] = self.ratio_likeDislike
        self['love_level'] = self.love_level

        return self
