import sqlite3
import os

import typer

from Counts.counts import count_items_by_author, count_num_distinct_authors, count_authors_per_item
from Items.get_all_items import get_all_items
from Visualizations.pie_chart import pie_chart

app = typer.Typer()

def get_connection(zotero_db_file: str):
    """Establish a connection to the SQLite database."""
    if not zotero_db_file:
        zotero_db_file = os.path.join(os.path.expanduser('~'), 'Zotero', 'zotero.sqlite') # cross-platform
    if not os.path.exists(zotero_db_file):
        raise FileNotFoundError(f"Database file not found: {zotero_db_file}")
    return sqlite3.connect(zotero_db_file)

@app.command()
def show_creators_per_item(zotero_db_file: str = typer.Option(None, help="Path to the Zotero SQLite database file.")):
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
def show_items_per_creator(zotero_db_file: str = typer.Option(None, help="Path to the Zotero SQLite database file."), 
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
def count_distinct_authors(zotero_db_file: str = typer.Option(None, help="Path to the Zotero SQLite database file.")):
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