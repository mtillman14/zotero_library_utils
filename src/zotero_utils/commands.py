import sqlite3
import os
from enum import Enum

import requests
import typer

from .Classes.item import get_item
from .Counts.counts import count_items_by_author, count_num_distinct_authors, count_authors_per_item
from .Items.get_all_items import get_all_item_ids
from .Visualizations.pie_chart import pie_chart
from .Visualizations.stacked_bar_chart import stacked_bar_chart
from .Visualizations.stem_plot import stem_plot

ZOTERO_DB_FILE_HELP = "Path to the Zotero SQLite database file."
VIS_TYPE_HELP = "Choose how to visualize the data."
NUM_GROUPS_HELP = "Number of groups to display in the chart."

ZOTERO_ENDPOINTS_DICT = {
    'items': '/items',
}

app = typer.Typer()

class VisType(str, Enum):
    """Enum to define the --vis-type options."""
    bar = "bar"
    pie = "pie"

def get_connection(zotero_db_file: str):
    """Establish a connection to the SQLite database."""
    if not zotero_db_file or isinstance(zotero_db_file, typer.models.OptionInfo):
        zotero_db_file = os.path.join(os.path.expanduser('~'), 'Zotero', 'zotero.sqlite') # cross-platform
    if not os.path.exists(zotero_db_file):
        raise FileNotFoundError(f"Database file not found: {zotero_db_file}")
    try:        
        return sqlite3.connect(zotero_db_file)
    except sqlite3.OperationalError:
        raise Exception("Zotero must be closed to connect to the database.")
    
def resolve_vis_type(vis_type: VisType):
    """Resolve the visualization type to a string. typer.models.OptionInfo is its type when not run from the command line."""
    if isinstance(vis_type, typer.models.OptionInfo):
        vis_type = vis_type.default        
    return vis_type.value

@app.command()
def show_creators_per_item(zotero_db_file: str = typer.Option(default=None, help=ZOTERO_DB_FILE_HELP),
                           num_groups: int = typer.Option(20, help=NUM_GROUPS_HELP),
                           vis_type: VisType = typer.Option(VisType.bar, help=VIS_TYPE_HELP)):
    """
    Show a chart of the number of creators per research item in the Zotero database.
    
    Args:
        zotero_db_file: Path to the Zotero SQLite database file.
    """
    conn = get_connection(zotero_db_file)
    try:        
        vis_type = resolve_vis_type(vis_type)
        item_ids = get_all_item_ids(conn)
        counts = count_authors_per_item(item_ids, conn)
        title_str = "Number of Authors Per Item"
        if vis_type=="bar":
            stacked_bar_chart(counts, num_groups=num_groups, sort_by='labels', title_str=title_str)
        elif vis_type=="pie":
            pie_chart(counts, num_groups=20, title_str=title_str, sort_by="labels")        
    finally:
        conn.close()

@app.command()
def show_items_per_creator(zotero_db_file: str = typer.Option(default=None, help=ZOTERO_DB_FILE_HELP), 
                           num_groups: int = typer.Option(20, help=NUM_GROUPS_HELP),
                           vis_type: VisType = typer.Option(VisType.bar, help=VIS_TYPE_HELP)):
    """
    Show a chart of the number of items from the top N creators in the Zotero database.
    
    Args:
        zotero_db_file: Path to the Zotero SQLite database file.
        num_groups: Number of groups to display in the chart (default is 20).
    """
    conn = get_connection(zotero_db_file)
    try:        
        vis_type = resolve_vis_type(vis_type)
        item_ids = get_all_item_ids(conn)
        counts = count_items_by_author(item_ids, conn)
        title_str = "Item Count Per Author"
        if vis_type=="bar":
            stacked_bar_chart(counts, num_groups=num_groups, sort_by='values', title_str=title_str)
        elif vis_type=="pie":
            pie_chart(counts, num_groups=num_groups, title_str=title_str, sort_by="values")        
    finally:
        conn.close()

@app.command()
def count_distinct_authors(zotero_db_file: str = typer.Option(default=None, help=ZOTERO_DB_FILE_HELP)):
    """
    Count the number of distinct authors in the Zotero database.
    
    Args:
        zotero_db_file: Path to the Zotero SQLite database file.
    """
    conn = get_connection(zotero_db_file)
    try:        
        item_ids = get_all_item_ids(conn)
        authors_count = count_num_distinct_authors(item_ids, conn)
        print(f"Number of authors: {authors_count}")
    finally:
        conn.close()


@app.command()
def show_timeline_date_published(zotero_db_file: str = typer.Option(default=None, help=ZOTERO_DB_FILE_HELP), 
                                 show_details: bool = typer.Option(default=True, help="Show the individual publications for each year. Hovering over each point reveals information about each individual publication.")):
    """
    Show the timeline of when the articles in the Zotero database were published.

    Args:
        zotero_db_file (str, optional): Path to the Zotero SQLite database file.
    """
    conn = get_connection(zotero_db_file)
    try:        
        item_ids = get_all_item_ids(conn)
        items_list = []
        for item_id in item_ids:
            item = get_item(item_id, conn)
            if item and item.date_published is not None:
                items_list.append(item)
        stem_plot([item.to_dict() for item in items_list], show_details=show_details)
    finally:
        conn.close()

@app.command()
def show_dag(zotero_db_file: str = typer.Option(default=None, help=ZOTERO_DB_FILE_HELP),
             save_path: str = typer.Option(default=None, help="Path to save the DAG.")
             ):
    """
    Show a directed acyclic graph of the relationships between items in the Zotero database.

    Args:
        zotero_db_file (str, optional): Path to the Zotero SQLite database file.
        save_path (str, optional): Path to save the DAG.
    """
    zotero_base_url = f"http://localhost:23119/api/zotero"
    zotero_endpoint = ZOTERO_ENDPOINTS_DICT['items']
    url = f"{zotero_base_url}{zotero_endpoint}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues
        
        # Parse the JSON response
        items = response.json()
        return items
    except requests.RequestException as e:
        print(f"Error fetching items: {e}")
        return None

    conn = get_connection(zotero_db_file)

    # 1. Get all of the Items of interest.
    try:
        item_ids = get_all_item_ids(conn)
        items_list = []
        for item_id in item_ids:
            item = get_item(item_id, conn)
            if item:
                items_list.append(item)
    except Exception as e:
        print(e)

    # 2. Get each Item's OpenAlex Work ID, store in a dict as item_id: work_id.
    work_ids = {}
    for item in items_list:
        work_ids[item.id] = item.get_open_alex_work_id()

    # 3. Ping the OpenAlex API (or cache) to get the references for each item. Parse them for citation information, stored as a dict, where keys and values are both OpenAlex Work ID's.
    # NOTE: Cache results in a .csv file to avoid pinging the API every time.
    cache_file = 'work_id_citations.csv'
    work_id_citations = {}
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            work_id_citations = {line.split(',')[0]: line.split(',')[1] for line in f.readlines()}
    for work_id in work_ids.values():
        if work_id in work_id_citations:
            continue # Skip if already cached.
        # Get the references for the work_id.
        # Parse the references for citation information.
        # Store the citation information in the dict.
        work_id_citations[work_id] = 'citation_info'

    with open(cache_file, 'w') as f:
        for work_id, citation_info in work_id_citations.items():
            f.write(f"{work_id},{citation_info}\n")

    # 4. Create the DAG from the dict using my base-dag library.

def main():
    """Entry point for the CLI when run as 'zotero-utils ...'"""
    app()