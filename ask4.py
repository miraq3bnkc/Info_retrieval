from collections import Counter
import os
import colbert
from colbert import Indexer
from colbert.infra import Run, RunConfig, ColBERTConfig

docs_directory = 'docs/' #path to your directory containing the documents

collection = []  #List containing 1209 documents
line_counts=[] #it stores how many lines each doc has

# Iterate through all files in the directory
for filename in os.listdir(docs_directory):
    filepath = os.path.join(docs_directory, filename)

    with open(filepath, 'r', encoding='utf-8') as file:
        # Read the contents of the file and append it to the collection
        content = file.read()
        collection.append(content)

        #calculate number of lines and store them to line_counts list
        lines=content.split('\n')  # Split content into lines
        line_counts.append(len(lines))

# Calculate the most common number of lines among the documents
common_line_count = Counter(line_counts).most_common(1)
doc_maxlen = common_line_count[0][0] if common_line_count else 300  # Default to 300 if no line count data
#doc_maxlen truncates docs at a number of tokens


checkpoint = 'colbert-ir/colbertv2.0'
nbits = 2   # encode each dimension with 2 bits
max_id = 1209  # Number of documents in the small collection

index_name = 'collection_index'

if __name__=='__main__':

        # Indexing
    with Run().context(RunConfig(nranks=1, experiment='notebook')):
        config = ColBERTConfig(doc_maxlen=doc_maxlen, nbits=2, kmeans_niters=4)

        indexer = Indexer(checkpoint=checkpoint, config=config)
        indexer.index(name=index_name, collection=collection[:max_id], overwrite=True)
    indexer.get_index()  # Get the absolute path of the index, if needed
