import json


class Story(dict):
    id: int
    text: str
    dicenumber:int
    roll: list

    date: str
    likes: int
    dislikes:int
    author_id: int

    def __init__(self, storydict: dict):
        super().__init__()
        self.id = storydict['id']
        self.text = storydict['text']
        self.dicenumber = storydict['dicenumber']
        self.roll = storydict['roll']
        self.date = storydict['date']
        self.likes = storydict['likes']
        self.dislikes = storydict['dislikes']
        self.author_id = storydict['author_id']


class Stories(dict):
    storylist:list

    def __init__(self, jpayload: json):
        super().__init__()
        storiesdict = json.loads(str(jpayload, 'utf8'))

        for s in storiesdict:
            story: Story = Story(s)
            self.storylist.append(story)
