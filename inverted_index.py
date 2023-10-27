import os
import pandas as pd

path ='docs'
os.chdir(path) #change directory so that we can see files inside of 'docs' 
#in order to count the number of files in docs folder 
#we know there are only txt files in that folder 
docs = os.listdir()

data = []  # Create a list to store dictionaries for each term
terms = set()  # Use a set to store unique terms

for doc_id in docs:
    with open(doc_id, "r") as f:
        text = f.read()
        tokens = text.split()
        terms.update(tokens)  # Add terms to the set

        for term in set(tokens):  # Use a set to get unique terms per document
            term_frequency = tokens.count(term)
            document_info = [doc_id, term_frequency]
            data.append({'Term': term, 'DocumentInfo': document_info})

os.chdir('..') #so that we are in the main directory of the project
#every word used in the C.F. collection is stored at lexicon.txt file
# Create a DataFrame by concatenating the list of dictionaries
inverted_index = pd.DataFrame(data)

# Group and aggregate the DocumentInfo column
inverted_index = inverted_index.groupby('Term')['DocumentInfo'].apply(list).reset_index()

# Save the DataFrame to a CSV file
inverted_index.to_csv('inverted_index.csv', index=False)