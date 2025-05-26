import os
import json

import tiktoken

MAX_TOKENS = 1000  # Maximum number of tokens for chunks

def num_tokens_from_string(string: str) -> int:
    """
    Returns the number of tokens in a string using the cl100k_base encoding."""

    encoding = tiktoken.get_encoding(encoding_name="cl100k_base")
    num_tokens = len(encoding.encode(string, disallowed_special=()))
    return num_tokens


def split_content_into_chunks(content: str, max_tokens: int) -> list:
    """
    Splits the content into smaller chunks, each with a maximum of `max_tokens` tokens.
    """
    encoding = tiktoken.get_encoding(encoding_name="cl100k_base")
    tokens = encoding.encode(content, disallowed_special=())
    chunks = []
    start = 0

    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]
        chunk = encoding.decode(chunk_tokens)
        chunks.append(chunk)
        start = end

    return chunks

def split_chapters(input_file, output_dir, chapters, max_tokens=MAX_TOKENS):
    """
    Splits the text file into chunks based on the chapters object and saves them as separate files.

    Args:
        input_file (str): Path to the input text file.
        output_dir (str): Directory to save the chapter files.
        chapters (list): List of dictionaries containing chapter metadata.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Read the input file into a list of lines
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    chapter_chunks = []

    # Iterate through the chapters and create chunks
    for i, chapter in enumerate(chapters):
        print(f"processing chapter {i + 1} of {len(chapters)}: {chapter['book']}-{chapter['chapter']}-{chapter['chapter_name']}")
        start_line = chapter["starting_line"] - 1  # Convert to zero-based index
        end_line = chapters[i + 1]["starting_line"] - 2 if i + 1 < len(chapters) else len(lines) - 1

        # Extract the chapter content
        chapter_content = lines[start_line:end_line + 1]
        chapter_content_str = ''.join(chapter_content)

        # check if chapter exceeds MAX_TOKENS

        n_tokens = num_tokens_from_string(chapter_content_str)


        if n_tokens > max_tokens:
            # Create a filename based on the book and chapter number
            filename = f"book_{chapter['book']}_chapter_{chapter['chapter']}.txt"
            print(f'Chapter {chapter["chapter"]} has {n_tokens} tokens which is more than {max_tokens} tokens. Splitting into parts...')
            chunks = split_content_into_chunks(chapter_content_str, max_tokens)

            # Save each chunk with a new name
            base_name, _ = os.path.splitext(filename)
            for idx, chunk in enumerate(chunks):
                part_suffix = chr(97 + idx)  # 'a', 'b', 'c', etc.
                new_filename = f"{base_name}_{part_suffix}.txt"

                with open(os.path.join(output_dir, new_filename), 'w', encoding='utf-8') as chunk_file:
                    chunk_file.write(chunk)
                
                ## update chapters list with new filenames
                sub_chapter = {
                "book": chapter["book"],
                "book_name": chapter["book_name"],
                "chapter": f'{chapter["chapter"]}_{part_suffix}',
                "chapter_name": chapter["chapter_name"],
                "file": new_filename,}

                chapter_chunks.append(sub_chapter)

        else:
            # Create a filename based on the book and chapter number
            filename = f"book_{chapter['book']}_chapter_{chapter['chapter']}.txt"
            # Write the chapter content to a file
            with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as out_file:
                out_file.writelines(chapter_content)

            chapter = {
                "book": chapter["book"],
                "book_name": chapter["book_name"],
                "chapter": chapter["chapter"],
                "chapter_name": chapter["chapter_name"],
                "file": filename
                }
            chapter_chunks.append(chapter)

            

    print(f"Splitting completed! Files saved in '{output_dir}'.")

    with open("chapters.json", "w", encoding="utf-8") as json_file:
        json.dump(chapter_chunks, json_file, indent=4)




