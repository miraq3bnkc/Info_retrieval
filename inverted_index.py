import os

path ='docs'
os.chdir(path) #change directory so that we can see files inside of 'docs' 
#in order to count the number of files in docs folder 
#we know there are only txt files in that folder 
docs = os.listdir()
num_files = len(docs)

inverted_index= {} #initialization of empty dictionary that will represent the inverted index
terms=[] #initialization of empty list of terms in docs

for doc_id in docs :
    with open(doc_id, "r") as f: #open every file in "docs" to read
        text=f.read()
        tokens=text.split(); #Split the text into words using spaces as the delimiter
        terms = list(set(tokens))# Combine the tokens into a list of unique terms
        for term in terms:
            if term in inverted_index:
                # If the term exists in the index, add the document ID and term frequency to its list
                term_entry = [doc_id, tokens.count(term)]
                inverted_index[term].append(term_entry)
            else:
                # If the term does not exist in the index, create a new entry with a list containing document ID and term frequency
                inverted_index[term] = [[doc_id, tokens.count(term)]]

os.chdir('..') #so that we are in the main directory of the project
#every word used in the C.F. collection is stored at lexicon.txt file
with open("lexicon.txt", "w+") as file:
    for term, postings in inverted_index.items():
        # Write the term to the file
        file.write(f"{term}:\n")

        # Write the postings list (document IDs and frequencies)
        for posting in postings:
            file.write(f"  Document {posting[0]}: {posting[1]}\n")
