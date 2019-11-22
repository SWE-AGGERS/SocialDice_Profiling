import requests

from classes.Errors import UserException
from classes.Stories import Stories
from classes.User import User

ENDPOINT_USER = 'http://0.0.0.0:5001/user/'

ENDPOINT_STORIES = 'http://0.0.0.0:5001/stories/'


def getStories(id:int):
    req = requests.get(url=ENDPOINT_STORIES+str(id))
    if req.status_code != 200:
        return None

    stories: Stories = Stories(req.json())

    return stories


def getUser(id: int):
    req = requests.get(url=ENDPOINT_USER + str(id))
    if req.status_code != 200:
        raise UserException()
    u: User = User(req.json())

    return u
