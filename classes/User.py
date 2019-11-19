import json


class User():
    id: int
    email: str
    firstname: str
    lastname: str

    def __init__(self, jpayload: json):
        userdict = json.loads(str(jpayload, 'utf8'))
        self.id = userdict['id']
        self.email = userdict['email']
        self.firstname = userdict['firstname']
        self.lastname = userdict['lastname']
