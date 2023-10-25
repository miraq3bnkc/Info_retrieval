import os

path ='docs'
os.chdir(path) #change directory so that we can see files inside of 'docs' 
#in order to count the number of files in docs folder 
#we know there are only txt files in that folder 
items = os.listdir()
num_files = len(items)

terms=[] #initialization of empty list of terms in docs

for item in items :
    with open(item, "r") as f: #open every file in "docs" to read
        text=f.read()
        tokens=text.split(); #Split the text into words using spaces as the delimiter
        terms = list(set(terms+tokens))# Combine the tokens into a list of unique terms

with open("words.txt", "w+") as file:
    for term in terms :
        file.write("%s\n" % term)
