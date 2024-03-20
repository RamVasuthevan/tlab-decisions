import PyPDF2
import os
import shutil


def extract():
    FILE_NAME = "../../data/2024-03-18/Toronto Local Appeal Body Combined Decisions - 2017.pdf"

    # Directly pass the file path to PdfReader
    reader = PyPDF2.PdfReader(FILE_NAME)
    print(f"Total pages: {len(reader.pages)}")
    return reader

def transform(reader):
   for bookmark in reader.outline:
       print(bookmark.title)

# Function to recursively extract bookmark details from the PDF outline
def extract_bookmarks(outlines, details, parent_title=""):
    for bookmark in outlines:
        if isinstance(bookmark, list):
            # Recursively process nested bookmarks
            extract_bookmarks(bookmark, details, parent_title)
        else:
            # Extract the title of the bookmark and calculate the full title
            title = bookmark.title
            full_title = f"{parent_title}{title}" if parent_title else title
            # Calculate the page number the bookmark points to (adding 1 to convert from 0-based to 1-based index)
            page_num = reader.get_destination_page_number(bookmark) + 1
            # Append the extracted details to the list
            details.append((full_title, page_num))

# Function to create new PDFs based on the extracted bookmarks and save them to the output directory
def load_splited_pdfs(reader):
    OUTPUT_DIR = "../../website/assets/tlab-decisions/2017"

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    bookmarks_details = []
    # Extract the bookmark details from the PDF
    extract_bookmarks(reader.outline, bookmarks_details)
    
    # Iterate over each bookmark to create and save a new PDF file
    for i, (title, start_page) in enumerate(bookmarks_details):
        writer = PyPDF2.PdfWriter()
        # Determine the end page for the current bookmark (start of the next bookmark or the end of the document)
        end_page = bookmarks_details[i + 1][1] - 1 if i + 1 < len(bookmarks_details) else len(reader.pages)
        
        # Add pages for the current bookmark to the new PDF
        for page_num in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page_num])
        
        # Create a valid filename from the bookmark title (limiting to the first 200 characters for simplicity)
        filename = f"{i:02}" + "_" + "".join(x for x in title if x.isalnum() or x in " ._") + ".pdf"
        # Construct the full file path
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Write the new PDF file to disk
        with open(filepath, 'wb') as outfile:
            writer.write(outfile)
        # Print a confirmation message
        #print(f"Extracted '{title}' to '{filepath}'")

def load_data_file(): 

if __name__ == "__main__":
    reader = extract()
    #transform(reader)
    load_splited_pdfs(reader)