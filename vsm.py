"""
This Python file aims to describe and generate a Vector Space Model (VSM) 
for a collection of 1209 documents related to C.F. available in the 'docs/'
directory. The queries used for comparison are located at "Queries_20.txt" 
file we will use the preprocessed and index information about the queries
located at "queries.csv". An inverted index that provides all the info we 
need about the collection is used and located at "inverted_index.csv"

The VSM creation is intended for information retrieval and similarity 
calculations between the queries and the documents in the C.F. collection.
"""


import ast
import math
import os
import numpy as np
import pandas as pd


#The function 'max_freq' calculates the maximum frequency of a term within a specified document or query. It takes two parameters:
# 'doc': Represents the identifier (ID) of the document or query under consideration.
# 'inverted_file': Refers to the inverted index containing information about terms, their frequencies, and associated documents/queries.

def max_freq(doc,inverted_file):
    max_freq=1
    for _, row in inverted_file.iterrows():
        doc_info = ast.literal_eval(row['Information'])
    
        for i in doc_info:
            doc_id, word_frequency = i
            if doc_id==doc :
                if max_freq<word_frequency:
                    max_freq=word_frequency
    return max_freq

def get_idf(inverted_file,documents):
    #get the terms we have
    terms=inverted_file['word'].to_list()
    #initialization of idf dataframe
    IDF = pd.Series(index=terms) 
    # Count the number of files (documents)
    N = len(documents)

    for _, row in inverted_file.iterrows():
        term = row['word']
        #we use ast because its read as a string without it 
        doc_info = ast.literal_eval(row['Information'])
        
        n = len(doc_info)  # Number of documents containing the term
        IDF[term] = math.log2(N / n) 
    return IDF


#this function calculates the TF-IDF for each term and document in an inverted index. It takes three parameters:
# 'inverted_file': refers to the inverted index , as you can tell by the name
# 'documents': is a list containing the ids' of documents we want to calculate tf-idf
# 'queries': is a boolean , when True we are calculating tf-idf for queries and so we have a different formula for tf 

def tf_idf(inverted_file,documents,queries,IDF):

    #get the terms we have
    terms=inverted_file['word'].to_list()

    #initialization of tf and idf dataframe
    TF=pd.DataFrame(0.0,columns=documents, index=terms) #filled with floating point zeros

    for _, row in inverted_file.iterrows():
        term = row['word']
        #we use ast because its read as a string without it 
        doc_info = ast.literal_eval(row['Information'])
        for i in doc_info:
            if queries==False:
                doc_id, word_frequency, positions = i  # Unpack the elements from i directly
                # word_frequency is equal to TF
                #calculate TF*IDF that gives as the VSM
                #we store the result of that multification in TF dataframe
                TF.loc[term, doc_id] = word_frequency*IDF[term]
            else:
                doc_id, word_frequency = i #we dont have positions
                tf_value = 0.5 + 0.5*word_frequency / max_freq(doc_id,inverted_file)
                TF.loc[term, doc_id] = tf_value*IDF[term]

    return TF

# Calculate document vectors cosine similarity with query vectors
def cosine_similarity(w1, w2):
    dot_product = np.dot(w1, w2)
    norm_w1 = np.linalg.norm(w1)
    norm_w2 = np.linalg.norm(w2)
    if norm_w1 != 0 and norm_w2 != 0:
        return dot_product / (norm_w1 * norm_w2)
    else:
        return 0  # Return a default value or handle as appropriate

'''
We will begin with the calculations of Term Frequency
and Inverse Document Frequency for the collection of 
documents. 
term frequency where TF=freq(i,j) and
inverse document frequency where IDF=log(N/n_i) '''

# Read the CSV files into a DataFrame (queries and docs respectively)
queries_inverted_index = pd.read_csv('queries.csv')
inverted_file = pd.read_csv('inverted_index.csv')

# Extract terms present in queries and documents
query_terms = set(queries_inverted_index['word'])
document_terms = set(inverted_file['word'])
# Find terms common in both queries and documents
common_terms = list(query_terms.intersection(document_terms))

# Filter documents and queries
docs_filtered = pd.merge(inverted_file, pd.DataFrame({'word': common_terms}), on='word')
queries_filtered = pd.merge(queries_inverted_index, pd.DataFrame({'word': common_terms}), on='word')

# Now docs_filtered and queries_filtered contain only terms that are present in the documents
# and queries respectively. Using only the terms present in both the queries and documents
# for the calculation of TF-IDF matrices ensures we wont make any unnecessary computations.
# Also, both tf-idf matrices having the same terms ensures that the vectors being compared 
# (for the cosine similarity) will have the same dimensions.

documents = sorted(os.listdir('docs'))
idf=get_idf(docs_filtered,documents)
tf_idf_docs=tf_idf(docs_filtered,documents, queries=False,IDF=idf)
# Save the DataFrame to a CSV file
tf_idf_docs.to_csv('vsm.csv', index=True)


'''
Now lets focus on the calculation of TF-IDF of the queries
For the queries Term Frequency formula will be:
TF = 0.5 + 0.5*freq(i,q) / max(freq(l,q))
and the formula for the IDF will be the same as 
for the collection of documents
'''

#Saving an id for the queries in a list
with open('Queries_20', 'r') as f:
    lines = f.readlines()
    queries_list = [i for i, _ in enumerate(lines, start=1)]

tf_idf_queries=tf_idf(queries_filtered, queries_list, queries=True,IDF=idf)
tf_idf_queries.to_csv('vsm_queries.csv', index=True)


# Calculate and store similarities for all queries in a dictionary
query_rankings = {}

for query_id in queries_list:
    similarities = []
    query_vector = tf_idf_queries.loc[:, query_id]

    for doc_id in documents:
        document_vector = tf_idf_docs.loc[:, doc_id]
        similarity = cosine_similarity(query_vector, document_vector)
        similarities.append((doc_id, similarity))
    
    # Sort similarities in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)
    query_rankings[query_id] = similarities[:100]  # Store top 5 similarities for each query

# Convert the similarity data into a DataFrame
data = {'Query': [], 'Document_ID': [], 'Rank': [], 'Similarity': []}
for query_id, sim_list in query_rankings.items():
    for rank, (doc_id, sim) in enumerate(sim_list, start=1):
        data['Query'].append(query_id)
        data['Document_ID'].append(doc_id)
        data['Rank'].append(rank)
        data['Similarity'].append(sim)

df_rankings = pd.DataFrame(data)

# Save DataFrame to a CSV file
df_rankings.to_csv('vsm_rankings.csv', index=False)