import os
import json

from file_split import split_chapters
import table_content
from create_embedings_vectors import get_chunk_object
from search_index import create_search_index, upload_chunk_document


# Example usage

input_file = "./progress_and_poverty_henry_george.txt"
output_text_chunks_directory = "./book_chunks"
output_vector_chunks_directory = "./data/embedings_chunks/"
search_index_name = "progress-poverty-index"


# delete index if it exists
# delete_index_if_exists(search_index_name)

# # STEP 1 -  Split the chapters and save them to files
# print("Splitting chapters...")
# split_chapters(input_file, output_text_chunks_directory, table_content.chapters)
# os.makedirs(output_vector_chunks_directory, exist_ok=True)

# # STEP 2 Create the chapters from the JSON file
# with open("chapters.json", "r") as f:
#     chapters = json.load(f)
# # Process each chapter and save the chunk object to a JSON file
# print("Processing chapters...")
# for i, chapter in enumerate(chapters):
#     print(f"Processing chapter {i+1}/{len(chapters)}: {chapter['file']}")
    
#     chunk = get_chunk_object(chapter, output_text_chunks_directory)

#     file_name = chapter["file"].split(".")[0]
#     # write chunk into JSON file into output directory
#     with open(f'{output_vector_chunks_directory}/{file_name}.json', 'w') as f:
#         json.dump(chunk, f, indent=4)

# # STEP 3 - Create the search index
# print("Creating search index...")
# create_search_index(search_index_name)
# print(f"Search index '{search_index_name}' created.")

# STEP 4 - Upload the chunks to the search index
print("Uploading chunks to search index...")
list_of_files = os.listdir(output_vector_chunks_directory)
for file in list_of_files:
    print(file)
    if file.endswith('.json'):
        filepath = os.path.join(output_vector_chunks_directory, file)
        upload_chunk_document(filepath, search_index_name)
        print(f"Uploaded {file} to search index.")




