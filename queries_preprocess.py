"""
In order to calculate the similarity of the queries to the collection
of C.F. documents (for the purposes of information retrieval), we will
need to preprocess the queries in the same way we did for the documents
in the creation of the inverted index. 
Queries are located at "Queries_10.txt"
"""
from inverted_index import generate_index_data, generate_inverted_index


queries=[]
#Saving the queries in a list
with open('Queries_20', 'r') as f:
    queries = f.readlines() #every line is a query

data = []  # Create a list to store dictionaries for each word
for index, query in enumerate(queries,start=1):
    query=query.lower().strip()
    #we need to lower the query because we have some uppercase letters
    data.extend(generate_index_data(index,query,query=True))


generate_inverted_index(data,'queries.csv')
