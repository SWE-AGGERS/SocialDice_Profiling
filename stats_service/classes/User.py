import json


class User(dict):
    id: int
    email: str
    firstname: str
    lastname: str

    def __init__(self, jpayload):
        super().__init__()
        if jpayload is None:
            self.user_id = 0
            self.email = ""
            self.firstname = ""
            self.lastname = ""
            return
        userdict = jpayload
        self.id = userdict['user_id']
        self.email = userdict['email']
        self.firstname = userdict['firstname']
        self.lastname = userdict['lastname']

    def jsonify(self):
        self['user_id'] = self.id
        self['email'] = self.email
        self['firstname'] = self.firstname
        self['lastname'] = self.lastname
        return self
