"""IN THIS PYTHON FILE WE WILL DESCRIBE AND 
CREATE A VECTOR SPACE MODEL FOR THE inverted_file.csv"""

import ast
import math
import os
import pandas as pd

# Read the CSV file into a DataFrame
inverted_file = pd.read_csv('inverted_index.csv')

terms=inverted_file['word'].to_list()
documents = os.listdir('docs')

#calculate term frequency where TF=f_ij and
#calculate inverse document frequency where IDF=log(N/n_i)

#initialization of tf and idf dictionaries
TF=pd.DataFrame(columns=terms, index=documents)
IDF=dict.fromkeys(terms) #create the keys for the dictionary of IDF 


documents = os.listdir('docs')
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
        TF.loc[doc_id, term] = word_frequency  # Assign word_frequency to TF DataFrame

'''Now that the information of the inverted file is ready 
will begin the calculations for TF and IDF'''


# Save the DataFrame to a CSV file
TF.to_csv('tf.csv', index=True)







