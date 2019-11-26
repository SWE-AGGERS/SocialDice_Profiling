import requests

from classes.Errors import UserException, StoriesException, ServiceUnreachable
from classes.Stories import Stories
from classes.User import User

ENDPOINT_USER = 'http://0.0.0.0:5042/user/'

ENDPOINT_STORIES = 'http://0.0.0.0:5042/stories/'



def getStories(id:int):
    print('Send request to ' + ENDPOINT_STORIES + ' to update story list')
    try:
        req = requests.get(url=ENDPOINT_STORIES+str(id), timeout=3)
        print('HTTP.GET executed')
    except TimeoutError:
        print('HTTP.GET FAIL!!!')
        # raise ServiceUnreachable('Story')
        print(ServiceUnreachable('Story'))

    if req.status_code != 200:
        print('Get stories fail with code:' + str(req.status_code))
        return Stories(None)

    stories: Stories = Stories(req.data)
    return stories


def getUser(id: int):
    print('Send request to ' + ENDPOINT_USER + ' to get user details')
    try:
        req = requests.get(url=ENDPOINT_USER + str(id), timeout=3)
        print('HTTP.GET executed')
    except TimeoutError:
        print('HTTP.GET FAIL!!!')
        raise ServiceUnreachable('User')

    if req.status_code != 200:
        raise UserException('Get user fail with code:' + str(req.status_code))
    u: User = User(req.data)

    return u
