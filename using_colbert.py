from collections import Counter
import os
import colbert
from colbert import Indexer
from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert.data import Queries
from colbert import Searcher

docs_directory = 'docs/' #path to your directory containing the documents

collection = []  #List containing 1209 documents
queries=[]

# Iterate through all files in the directory
for filename in sorted(os.listdir(docs_directory)):
    filepath = os.path.join(docs_directory, filename)

    with open(filepath, 'r', encoding='utf-8') as file:
        # Read the contents of the file and append it to the collection
        content = file.read()
        collection.append(content)

# Read the queries from the file into a list
with open('Queries_20', 'r') as file:
    queries = file.read().splitlines()

# Convert the list of queries into a dictionary format
queries_dict = {i: query for i, query in enumerate(queries,start=1)}


checkpoint = 'colbert-ir/colbertv2.0'
nbits = 2   # encode each dimension with 2 bits
max_id = 1209  # Number of documents in the small collection

index_name = 'collection_index'

if __name__=='__main__':

        # Indexing
    with Run().context(RunConfig(nranks=1, experiment='notebook')):
        config = ColBERTConfig( nbits=2)

        indexer = Indexer(checkpoint=checkpoint, config=config)
        indexer.index(name=index_name, collection=collection[:max_id], overwrite=True)
    
        searcher = Searcher(index=index_name, collection=collection)
        queries = Queries(data=queries_dict)
        ranking = searcher.search_all(queries, k=100)
        ranking.save("ranking.tsv")