"""IN THIS PYTHON FILE WE WILL DESCRIBE AND 
CREATE A VECTOR SPACE MODEL FOR THE inverted_file.csv"""

import ast
import math
import os
import pandas as pd

# Read the CSV file into a DataFrame
inverted_file = pd.read_csv('inverted_index.csv')

'''Now that the information of the inverted file is ready 
   will begin the calculations for TF and IDF

   calculate term frequency where TF=f_ij and
   calculate inverse document frequency where IDF=log(N/n_i) '''

#get the terms and documents we have
terms=inverted_file['word'].to_list()
documents = sorted(os.listdir('docs'))

#initialization of tf and idf dataframe
TF=pd.DataFrame(0.0,columns=documents, index=terms) #filled with floating point zeros
IDF = pd.Series(index=terms) 

# Count the number of files (documents)
N = len(documents)

for index, row in inverted_file.iterrows():
    term = row['word']
    #we use ast because its read as a string without it 
    doc_info = ast.literal_eval(row['DocumentInfo'])
    
    n = len(doc_info)  # Number of documents containing the term
    IDF[term] = math.log2(N / n) 
    for i in doc_info:
        doc_id, word_frequency, positions = i  # Unpack the elements from i directly
        # word_frequency is equal to TF
        #calculate TF*IDF that gives as the VSM
        #we store the result of that multification in TF dataframe
        TF.loc[term, doc_id] = word_frequency*IDF[term]


# Save the DataFrame to a CSV file
TF.to_csv('vsm.tsv',sep='\t', index=True)
