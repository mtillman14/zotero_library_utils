import re

REFERENCES_HEADER_STRS = [
    '**references**',
    'r e f e r e n c e s'
]
SEP = '\n'
REFERENCE_STARTS_STR = [
    "^\\d+\\.\\s", # Starts with any number, followed by a period, and a space.
    "^\\[\\d+\\]", # Starts with open square bracket, any number, closed square bracket.
    '^[A-Z]' # Starts with capital letter
]

def get_references_section(md_text: str) -> str:
    """Isolate the references section in Markdown text."""
    lower_md_text = md_text.lower()
    str_list_lower = lower_md_text.lower().split(SEP)
    index_found = False
    for ref_header_str in REFERENCES_HEADER_STRS:
        if index_found:
            break
        for index, string in enumerate(str_list_lower):
            if ref_header_str in string:
                references_header_index = index
                break
    if not references_header_index:
        raise ValueError("References section header not found.")
    str_list = md_text.split(SEP)

    # Get the other text in the references string besides the ref_header_str
    refs_section_header_lower = str_list_lower[references_header_index]
    ref_header_str_index = refs_section_header_lower.find(ref_header_str)
    section_break_marker_prefix = refs_section_header_lower[0:ref_header_str_index]
    section_break_marker_suffix = refs_section_header_lower[ref_header_str_index + len(ref_header_str):]

    # Get the index of the next section break after the references.
    for index, string in enumerate(str_list_lower[references_header_index+1:]):
        if string.startswith(section_break_marker_prefix) and string.endswith(section_break_marker_suffix):
            refs_section_end_index = index + references_header_index+1
            break
    return str_list[references_header_index+1:refs_section_end_index]

def isolate_references(references_text: list) -> list:
    """Given the references section as a list, return a list of reference strings."""
    in_ref = False
    reference = ''
    references_list = []
    for entry in references_text:
        if entry.endswith('_'):
            entry = entry[0:-1]
        if not in_ref:
            # Check if the current entry is the start of a reference.
            if any([re.match(ref_start_str, entry) for ref_start_str in REFERENCE_STARTS_STR]):
                in_ref = True
        if not in_ref:
            continue
        
        if reference and not reference.endswith(' ') and not entry.startswith(' '):
            entry = ' ' + entry
        reference = reference + entry

        if entry.endswith('.'):
            in_ref = False

        if not in_ref:
            references_list.append(reference)
            reference = ''

    # Fix the references list by ensuring that each reference has the same number of periods.
    # This assumes that at least one reference was properly and entirely captured by the method above, which seems reasonable.

    # Get the maximum number of periods in a reference in the reference list.
    end_sentence_regex = '\\S[a-zA-Z]\\. [A-Z]' # end of sentence regex
    max_period_count = 0
    for ref in references_list:
        matches = re.findall(end_sentence_regex, ref)
        period_count = len(matches) + 1
        if period_count > max_period_count:
            max_period_count = period_count

    # Append the items in the reference list together that don't have the right number of periods.
    references_list_corrected = []
    reference = ''
    for entry in references_list:
        reference += entry
        if reference.count('.') == max_period_count:
            references_list_corrected.append(reference)
            reference = ''            

    return references_list

        