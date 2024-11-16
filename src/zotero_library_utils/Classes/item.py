import datetime

class Item:

    def __init__(self,
                 title: str,
                 file_path: str = None,
                 creators: list = [],
                 publisher: str = None,
                 date_published: datetime.datetime = None,
                 date_added: datetime.datetime = None
                 ):
        self.title = title
        self.file_path = file_path
        self.creators = creators
        self.publisher = publisher
        self.date_published = date_published
        self.date_added = date_added