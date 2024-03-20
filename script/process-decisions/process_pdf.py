import PyPDF2
import os
import shutil
import yaml
from datetime import datetime

def extract():
    FILE_NAME = "../../data/2024-03-18/Toronto Local Appeal Body Combined Decisions - 2017.pdf"
    reader = PyPDF2.PdfReader(FILE_NAME)
    print(f"Total pages: {len(reader.pages)}")
    return reader

def transform_bookmarks(reader):
    bookmarks_details = []
    extract_bookmarks(reader.outline, bookmarks_details)
    
    decisions = []
    for i, (title, _) in enumerate(bookmarks_details):
        decisions.append({
            'bookmark_name': str(title),
            'year': "2017",
            'file_name': f"{i:02}_{''.join(x for x in title if x.isalnum() or x in ' ._-')}.pdf"
        })
    return decisions

def extract_bookmarks(outlines, details, parent_title=""):
    for bookmark in outlines:
        if isinstance(bookmark, list):
            extract_bookmarks(bookmark, details, parent_title)
        else:
            title = bookmark.title
            full_title = f"{parent_title}{title}" if parent_title else title
            page_num = reader.get_destination_page_number(bookmark) + 1
            details.append((full_title, page_num))

def load_splited_pdfs(reader, decisions):
    OUTPUT_DIR = "../../website/assets/tlab-decisions/2017"
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    bookmarks_details = []
    extract_bookmarks(reader.outline, bookmarks_details)
    
    for i, (title, start_page) in enumerate(bookmarks_details):
        writer = PyPDF2.PdfWriter()
        end_page = bookmarks_details[i + 1][1] - 1 if i + 1 < len(bookmarks_details) else len(reader.pages)
        for page_num in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page_num])
        filepath = os.path.join(OUTPUT_DIR, decisions[i]['file_name'])
        with open(filepath, 'wb') as outfile:
            writer.write(outfile)

def load_data_file(decisions):
    OUTPUT_FILE = "../../website/_data/decisions.yml"
    with open(OUTPUT_FILE, 'w') as file:
        yaml.dump(decisions, file, default_flow_style=False, sort_keys=False)

if __name__ == "__main__":
    reader = extract()
    decisions = transform_bookmarks(reader)
    load_splited_pdfs(reader, decisions)
    load_data_file(decisions)
