import datetime
import sqlite3
import re

from .creator import get_creator

ITEM_FIELDS = [
    "title",
    "file_path",
    "creators",
    "publisher",
    "date_published",
    "date_added"
]

class Item:

    def __init__(self,
                 title: str,
                 file_path: str = None,
                 creators: list = [],
                 publisher: str = None,
                 date_published: str = None,
                 date_added: str = None
                 ):
        self.title = title
        self.file_path = file_path
        self.creators = tuple(creators)
        self.publisher = publisher
        self.date_published = datetime.datetime.strptime(date_published, "%Y-%m-%d") if date_published is not None else None
        self.date_added = datetime.datetime.strptime(date_added, "%Y-%m-%d") if date_added is not None else None

    def __str__(self):
        first_creator_name = "No Creator"
        if self.creators:
            first_creator_name = self.creators[0]
        date_published = "No Date"
        if self.date_published:
            date_published = str(self.date_published.date())
        return f"{first_creator_name}, {date_published}"
    
    def __repr__(self):
        return self.__str__()


    def to_dict(self) -> dict:
        """Convert an Item object to its dictionary representation."""
        excluded_fields = ["file_path"]
        item_dict = {}
        for field, value in self.__dict__.items():
            if field in excluded_fields:
                continue
            if value is None:
                value = "None"
            item_dict[field] = value
        return item_dict
    
def get_item(item_id: int, conn: sqlite3.Connection) -> Item:
    """Return an Item object given an item ID."""

    sqlite_str = """SELECT dateAdded, dateModified FROM items WHERE itemID = ?"""
    cursor = conn.cursor()
    sql_result = cursor.execute(sqlite_str, (item_id,)).fetchone()    
    date_added = sql_result[0]
    date_modified = sql_result[1]

    # Get the item data field & value IDs
    sqlite_str = """SELECT fieldID, valueID FROM itemData WHERE itemID = ?"""
    sql_result = cursor.execute(sqlite_str, (item_id,)).fetchall()
    field_ids_value_ids = {row[0]: row[1] for row in sql_result}

    if not field_ids_value_ids:
        return None

    # Get the field names
    field_ids = [k for k in field_ids_value_ids.keys()]
    value_ids = [v for v in field_ids_value_ids.values()]
    num_fields = len(tuple(set(field_ids)))
    field_params = "?, " * num_fields
    field_params = field_params[0:-2]
    sqlite_str = f"""SELECT fieldID, fieldName FROM fields WHERE fieldID IN ({field_params})"""
    sql_result = cursor.execute(sqlite_str, field_ids).fetchall()
    field_ids_field_names = {row[0]: row[1] for row in sql_result}

    # Get the values    
    value_params = field_params
    sqlite_str = f"""SELECT valueID, value FROM itemDataValues WHERE valueID IN ({value_params})"""
    sql_result = cursor.execute(sqlite_str, value_ids).fetchall()
    value_ids_values = {row[0]: row[1] for row in sql_result}

    item_dict = {
        field_ids_field_names[k]: value_ids_values[v] for k, v in field_ids_value_ids.items()
    }

    item_dict_clean = {k: v for k, v in item_dict.items() if k in ITEM_FIELDS}

    if "title" not in item_dict_clean:
        return None    
    
    # Get the creators of the item.
    sqlite_str = """SELECT creatorID FROM itemCreators WHERE itemID = ?"""
    creator_ids = cursor.execute(sqlite_str, (item_id,)).fetchone()
    creators = []
    if creator_ids:
        creators = [get_creator(creator_id, conn) for creator_id in creator_ids]

    item_dict_clean["creators"] = [", ".join([creator.last_name, creator.first_name]) for creator in creators]

    if "date" in item_dict:
        date_pattern = r'\d{4}-\d{2}-\d{2}'
        matches = re.search(date_pattern, item_dict["date"])
        date_published = matches.group(0)
        date_published = re.sub('-00', '-01', date_published)
        item_dict_clean["date_published"] = date_published
        

    return Item(**item_dict_clean)