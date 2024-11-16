# def main():    
#     pass

# if __name__ == '__main__':
#     main()

import sqlite3

from Counts.counts import count_items_by_author
from Items.get_all_items import get_all_items

db = "/Users/mitchelltillman/Zotero/zotero.sqlite"
conn = sqlite3.connect(db)
item_ids = get_all_items(conn)
counts = count_items_by_author(item_ids, conn)
print(counts)

# from Parse_PDFs.pdf2md import pdf2md
# from Parse_PDFs.extract_references import get_references_section

# file_path = "/Users/mitchelltillman/Zotero/storage/2AQ36IHF/McGinnis and Perkins - 2012 - A Highly Miniaturized, Wireless Inertial Measureme.pdf"
# md_text = pdf2md(file_path)
# refs_section = get_references_section(md_text)
# print(refs_section)