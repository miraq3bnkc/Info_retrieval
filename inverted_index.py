import os

#in order to count the number of files in docs folder 
#we know there are only txt files in that folder 
items = os.listdir('docs')
num_files = len(items)

terms=[] #initialization of empty list of terms in docs

for item in items :
    f = open(item, "r") #open every file in "docs" to read
    tokens=f.split(); #Split the text into words using spaces as the delimiter
    terms = list(set(terms+tokens))# Combine the tokens into a list of unique terms

print(f'The folder docs contains {num_files} files.')
print(terms)