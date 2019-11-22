import json


class User(dict):
    id: int
    email: str
    firstname: str
    lastname: str

    def __init__(self, jpayload: bytes):
        super().__init__()
        if jpayload is None:
            self.id = 0
            self.email = ""
            self.firstname = ""
            self.lastname = ""
            return
        userdict = json.loads(str(jpayload, 'utf8'))
        self.id = userdict['id']
        self.email = userdict['email']
        self.firstname = userdict['firstname']
        self.lastname = userdict['lastname']

    def jsonify(self):
        self['id'] = self.id
        self['email'] = self.email
        self['firstname'] = self.firstname
        self['lastname'] = self.lastname
        return self
