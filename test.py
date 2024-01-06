import os


docs_directory = 'docs/' #path to your directory containing the documents

doc_filenames = []  # List to store filenames

# Iterate through all files in the directory in numerical order
for filename in sorted(os.listdir(docs_directory)):
    filepath = os.path.join(docs_directory, filename)

    with open(filepath, 'r', encoding='utf-8') as file:
        # Read the contents of the file and append it to the collection
        content = file.read()
        doc_filenames.append(filename)  # Storing filenames separately

# Print filenames and their respective indices
for index, filename in enumerate(doc_filenames[:196]):
    print(f"Index: {index}, Filename: {filename}")