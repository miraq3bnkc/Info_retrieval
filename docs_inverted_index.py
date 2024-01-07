import os
from inverted_index import generate_index_data, generate_inverted_index

path ='docs'
os.chdir(path) #change directory so that we can see files inside of 'docs' 
#in order to count the number of files in docs folder 
#we know there are only txt files in that folder 
docs = os.listdir()

data = []  # Create a list to store dictionaries for each word
for doc_id in docs:
    with open(doc_id, "r") as f:
        text = f.read()
        data.extend(generate_index_data(doc_id,text,query=False))

os.chdir('..') #so that we are in the main directory of the project
#every word used in the C.F. collection is stored at inverted_index.csv file, in the column "words"
generate_inverted_index(data,"inverted_index.csv")