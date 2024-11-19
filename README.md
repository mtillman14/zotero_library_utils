# zotero_library_utils

This project aims to provide tools to understand the makeup of a Zotero library - entirely locally - by reading from Zotero's SQLite database. This package focuses on providing tools that Zotero itself does not provide.

# Installation
```bash
pip install zotero_library_utils
```

# Tools
## Counts
Provides counts of several pieces of metadata:
    
1. Number of articles from each author. Optionally, you can specify the number of slices shown.
```bash
python -m zotero_library_utils show-items-per-creator --num-slices=20
```
![Number of Articles from Top 20 Authors](docs/show_items_per_creator.png)

2. Number of different authors in the database (identified by first and last name)
```bash
python -m zotero_library_utils count-distinct-authors
```

3. Number of articles with 1-N authors. Optionally, you can specify the number of slices shown.
```bash
python -m zotero_library_utils show-creators-per-item --num-slices=20
```
![Number of Authors Per Article](docs/show_creators_per_item.png)

## Timelines
Visualize when articles were published
```bash
python -m zotero_library_utils show-timeline-date-published --show-details=false
```
![Article Publication Timeline](docs/article_publication_timeline.png)

<!-- ## Reference Graphs (Not Implemented)
!!!warning
    Not currently implemented. Parsing PDF's is difficult!
This feature will attempt to create a graph of the references using AI locally to read the PDF's. The result will be similar to many existing cloud-based, closed-source tools, however this tool is entirely open-source, local, and reads your entire Zotero library to allow you to spot trends and gaps in your collection. -->

# Contributing
For errors and feature suggestions, please open an issue. Pull requests are also appreciated and will be reviewed ASAP.

# Roadmap
I'd like to be able to build a graph of the references between items in the Zotero database. Sticking to the local-first design, this means parsing PDF's for their references, which is a notoriously difficult problem. Any suggestions are welcome, please open an issue!