import sqlite3
import os

import typer

from .Classes.item import get_item
from .Counts.counts import count_items_by_author, count_num_distinct_authors, count_authors_per_item
from .Items.get_all_items import get_all_items
from .Visualizations.pie_chart import pie_chart
from .Visualizations.stem_plot import stem_plot

ZOTERO_DB_FILE_HELP = "Path to the Zotero SQLite database file."

app = typer.Typer()

def get_connection(zotero_db_file: str):
    """Establish a connection to the SQLite database."""
    if not zotero_db_file:
        zotero_db_file = os.path.join(os.path.expanduser('~'), 'Zotero', 'zotero.sqlite') # cross-platform
    if not os.path.exists(zotero_db_file):
        raise FileNotFoundError(f"Database file not found: {zotero_db_file}")
    try:        
        return sqlite3.connect(zotero_db_file)
    except sqlite3.OperationalError:
        raise Exception("Zotero is must be closed to connect to the database.")

@app.command()
def show_creators_per_item(zotero_db_file: str = typer.Option(default=None, help=ZOTERO_DB_FILE_HELP)):
    """
    Show a pie chart of the number of creators per research item in the Zotero database.
    
    Args:
        zotero_db_file: Path to the Zotero SQLite database file.
    """
    try:
        conn = get_connection(zotero_db_file)
        item_ids = get_all_items(conn)
        counts = count_authors_per_item(item_ids, conn)
        title_str = "Number of Authors Per Item"
        pie_chart(counts, num_slices=20, title_str=title_str, sort_by="labels")
    finally:
        conn.close()

@app.command()
def show_items_per_creator(zotero_db_file: str = typer.Option(default=None, help=ZOTERO_DB_FILE_HELP), 
                           num_slices: int = typer.Option(20, help="Number of slices to display in the pie chart.")):
    """
    Show a pie chart of the number of items from the top N creators in the Zotero database.
    
    Args:
        zotero_db_file: Path to the Zotero SQLite database file.
        num_slices: Number of slices to display in the pie chart (default is 20).
    """
    try:
        conn = get_connection(zotero_db_file)
        item_ids = get_all_items(conn)
        counts = count_items_by_author(item_ids, conn)
        title_str = "Item Count Per Author"
        pie_chart(counts, num_slices=num_slices, title_str=title_str, sort_by="values")
    finally:
        conn.close()

@app.command()
def count_distinct_authors(zotero_db_file: str = typer.Option(default=None, help=ZOTERO_DB_FILE_HELP)):
    """
    Count the number of distinct authors in the Zotero database.
    
    Args:
        zotero_db_file: Path to the Zotero SQLite database file.
    """
    try:
        conn = get_connection(zotero_db_file)
        item_ids = get_all_items(conn)
        authors_count = count_num_distinct_authors(item_ids, conn)
        print(f"Number of authors: {authors_count}")
    finally:
        conn.close()


@app.command()
def show_timeline_date_published(zotero_db_file: str = typer.Option(default=None, help=ZOTERO_DB_FILE_HELP), 
                                 show_details: bool = typer.Option(default=True, help="true to show the individual publications for each year.")):
    """
    Show the timeline of when the articles in the Zotero database were published.

    Args:
        zotero_db_file (str, optional): Path to the Zotero SQLite database file.
    """
    try:
        conn = get_connection(zotero_db_file)
        item_ids = get_all_items(conn)
        items_list = []
        for item_id in item_ids:
            item = get_item(item_id, conn)
            if item and item.date_published is not None:
                items_list.append(item)
        stem_plot([item.to_dict() for item in items_list], show_details=show_details)
    finally:
        conn.close()

def main():
    """Entry point for the CLI when run as 'zotero-utils ...'"""
    app()