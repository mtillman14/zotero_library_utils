import sys
print(sys.path)

from zotero_library_utils.Parse_PDFs.pdf2md import pdf2md
from zotero_library_utils.Parse_PDFs.extract_references import get_references_section

file_path = "/Users/mitchelltillman/Zotero/storage/2AQ36IHF/McGinnis and Perkins - 2012 - A Highly Miniaturized, Wireless Inertial Measureme.pdf"
md_text = pdf2md(file_path)
refs_section = get_references_section(md_text)