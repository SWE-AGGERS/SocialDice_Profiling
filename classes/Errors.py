class UserException(Exception):
    def __init__(self):
        var = self.args


class StoriesException(Exception):
    def __init__(self):
        var = self.args


class NoUser(dict):
    def __init__(self):
        super().__init__()
        self['code'] = 404
        self['status'] = 'error'
        self['data'] = 'User not exist'


class NoStats(dict):
    def __init__(self):
        super().__init__()
        self['code'] = 403
        self['status'] = 'error'
        self['data'] = 'Stats not ready'
