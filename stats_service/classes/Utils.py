import requests

from stats_service.classes.Errors import UserException, StoriesException, ServiceUnreachable
from stats_service.classes.Stories import Stories
from stats_service.classes.User import User

from stats_service.constants import USER_URL, STORIES_URL


def getStories(story_id:int):
    print('Send request to ' + STORIES_URL + ' to update story list')
    try:
        req = requests.get(url=STORIES_URL+str(story_id), timeout=3)
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


def getUser(user_id: int):
    print('Send request to ' + USER_URL + ' to get user details')
    try:
        req = requests.get(USER_URL + str(user_id), timeout=3)
        print('HTTP.GET executed')
    except TimeoutError:
        print('HTTP.GET FAIL!!!')
        raise ServiceUnreachable('User')

    if req.status_code != 200:
        raise UserException('Get user fail with code:' + str(req.status_code))
    u: User = User(req.json())

    return u
