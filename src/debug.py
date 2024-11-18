# src/debug_commands.py
import sys
from pathlib import Path

# Add the src directory to Python path to make the package imports work
src_dir = str(Path(__file__).parent)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from zotero_library_utils.commands import show_timeline_date_published

def main():
    # You can set breakpoints in this function
    zotero_db_path = None  # Set this to your database path if needed
    show_timeline_date_published()

if __name__ == "__main__":
    main()