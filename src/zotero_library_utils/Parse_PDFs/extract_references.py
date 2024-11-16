
REFERENCES_HEADER_STR = '**references**'
SEP = '\n'

def get_references_section(md_text: str):
    """Isolate the references section in Markdown text."""
    lower_md_text = md_text.lower()
    str_list_lower = lower_md_text.lower().split(SEP)
    references_header_index = str_list_lower.index(REFERENCES_HEADER_STR)
    str_list = md_text.split(SEP)
    return str_list[references_header_index+1:]
