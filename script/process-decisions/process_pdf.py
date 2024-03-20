import PyPDF2
import os
import shutil
import yaml
from pprint import pprint

def extract(file_name):
    reader = PyPDF2.PdfReader(file_name)
    return reader

def transform_bookmarks(reader, year, file_name):
    bookmarks_details = []
    extract_bookmarks(year,reader.outline, bookmarks_details, reader)
    
    # Extract the year directly from the file name instead of reader object
    year = os.path.basename(file_name).split(' ')[-1].split('.')[0]
    
    decisions = []
    for i, (title, _) in enumerate(bookmarks_details):
        decisions.append({
            'bookmark_name': str(title),
            'year': year,
            'file_name': f"{i:02}_{''.join(x for x in title if x.isalnum() or x in ' ._-')}.pdf"
        })
    return decisions

# Adjust the extract_bookmarks function to accept reader as an argument
def extract_bookmarks(year,outlines, details, reader, parent_title=""):
    for bookmark in outlines:
        if isinstance(bookmark, list):
            if year=="2018":
                extract_bookmarks(year,bookmark, details, reader, parent_title)
        else:
            title = bookmark.title
            full_title = f"{parent_title}{title}" if parent_title else title
            page_num = reader.get_destination_page_number(bookmark) + 1
            details.append((full_title, page_num))

def load_splited_pdfs(reader, decisions, year):
    OUTPUT_DIR = f"../../website/assets/tlab-decisions/{year}"
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    bookmarks_details = []
    extract_bookmarks(year, reader.outline, bookmarks_details, reader)
    
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
    files_to_process = {
#                            "2017":"../../data/2024-03-18/Toronto Local Appeal Body Combined Decisions - 2017.pdf",
                            "2018":"../../data/2024-03-18/Toronto Local Appeal Body Combined Decisions - 2018.pdf",
#                            "2019":"../../data/2024-03-18/Toronto Local Appeal Body Combined Decisions - 2019.pdf",
#                            "2020":"../../data/2024-03-18/Toronto Local Appeal Body Combined Decisions - 2020.pdf",
#                            "2021":"../../data/2024-03-18/Toronto Local Appeal Body Combined Decisions - 2021.pdf",
#                            "2022":"../../data/2024-03-18/Toronto Local Appeal Body Combined Decisions - 2022.pdf",
                        }
    
    output_file_path = "../../website/_data/decisions.yml"
    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    all_decisions = []
    for year, file_path in files_to_process.items():
        reader = extract(file_path)
        decisions = transform_bookmarks(reader, year, file_path)
        load_splited_pdfs(reader, decisions, year)
        all_decisions.extend(decisions)

    load_data_file(all_decisions)
