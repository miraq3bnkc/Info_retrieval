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
import pandas as pd


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

def tf_idf(inverted_file,documents,queries):

    #get the terms we have
    terms=inverted_file['word'].to_list()

    #initialization of tf and idf dataframe
    TF=pd.DataFrame(0.0,columns=documents, index=terms) #filled with floating point zeros
    IDF = pd.Series(index=terms) 

    # Count the number of files (documents)
    N = len(documents)

    for _, row in inverted_file.iterrows():
        term = row['word']
        #we use ast because its read as a string without it 
        doc_info = ast.literal_eval(row['Information'])
        
        n = len(doc_info)  # Number of documents containing the term
        IDF[term] = math.log2(N / n) 
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

'''
We will begin with the calculations of Term Frequency
and Inverse Document Frequency for the collection of 
documents. 
term frequency where TF=freq(i,j) and
inverse document frequency where IDF=log(N/n_i) '''

# Read the CSV files into a DataFrame
inverted_file = pd.read_csv('inverted_index.csv')
documents = sorted(os.listdir('docs'))

tf_idf_docs=tf_idf(inverted_file,documents, queries=False)
# Save the DataFrame to a CSV file
tf_idf_docs.to_csv('vsm.csv', index=True)


'''
Now lets focus on the calculation of TF-IDF of the queries
For the queries Term Frequency formula will be:
TF = 0.5 + 0.5*freq(i,q) / max(freq(l,q))
and the formula for the IDF will be the same as 
for the collection of documents
'''

queries_inverted_index = pd.read_csv('queries.csv')
#Saving an id for the queries in a list
with open('Queries_20', 'r') as f:
    lines = f.readlines()
    queries_list = [i for i, _ in enumerate(lines, start=1)]
    #every query will have and id from q1 to qN , where N equals to the number of queries


tf_idf_queries=tf_idf(queries_inverted_index, queries_list, queries=True)
tf_idf_queries.to_csv('vsm_queries.csv', index=True)
