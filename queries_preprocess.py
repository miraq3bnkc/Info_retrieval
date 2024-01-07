"""
In order to calculate the similarity of the queries to the collection
of C.F. documents (for the purposes of information retrieval), we will
need to preprocess the queries in the same way we did for the documents
in the creation of the inverted index. 
Queries are located at "Queries_10.txt"
"""

import os
import pandas as pd
from nltk.stem import SnowballStemmer
from word_conversion import words_to_numbers


queries=[]
#Saving the queries in a list
with open('Queries_20', 'r') as f:
    queries = f.readlines() #every line is a query

# Create a SnowballStemmer for English (Porter2)
porter2 = SnowballStemmer('english')


data = []  # Create a list to store dictionaries for each word
words = []  # Use a set to store unique words

for index, query in enumerate(queries,start=1):
    query=query.lower().strip()
    #we need to lower the query because we have some uppercase letters
    tokens = query.split() # split so as to get all the words of the query
    tokens=  words_to_numbers(tokens)
    
    stemmed_tokens = [porter2.stem(token) for token in tokens]  # Stemming the tokens
    words=set(stemmed_tokens)  # Add words to the set , so as to not have duplicates

    for word in words:  # Use a set to get unique words per document
        word_frequency = stemmed_tokens.count(word)
        #we arent trying to make a fully inverted index , so we will not save the positions this time
        word_info = [index, word_frequency] # Information per word in query
        data.append({'word': word, 'Information': word_info})

# Create a DataFrame by concatenating the list of dictionaries
inverted_index = pd.DataFrame(data)

# Group and aggregate the DocumentInfo column
inverted_index = inverted_index.groupby('word')['Information'].apply(list).reset_index()

# Save the DataFrame to a CSV file
inverted_index.to_csv('queries.csv', index=False)