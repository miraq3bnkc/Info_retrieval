import os
import pandas as pd
from nltk.stem import SnowballStemmer
from word_conversion import words_to_numbers
'''from nltk.corpus import stopwords

# Download NLTK stopwords 
import nltk
nltk.download('stopwords')

leaving out for now'''

path ='docs'
os.chdir(path) #change directory so that we can see files inside of 'docs' 
#in order to count the number of files in docs folder 
#we know there are only txt files in that folder 
docs = os.listdir()

# Create a SnowballStemmer for English (Porter2)
porter2 = SnowballStemmer('english')

# Get the list of English stop words
#stop_words = set(stopwords.words('english'))

data = []  # Create a list to store dictionaries for each word
words = []  # Use a set to store unique words

for doc_id in docs:
    with open(doc_id, "r") as f:
        text = f.read()
        tokens = text.split() # split so as to get all the words of the doc
        tokens=  words_to_numbers(tokens)
        
        # Remove stop words and punctuation
        #tokens = [word.lower() for word in tokens if word.lower() not in stop_words]

        stemmed_tokens = [porter2.stem(token) for token in tokens]  # Stemming the tokens
        words=set(stemmed_tokens)  # Add words to the set , so as to not have duplicates

        for word in words:  # Use a set to get unique words per document
            word_frequency = stemmed_tokens.count(word)
            positions = [index for index, token in enumerate(stemmed_tokens,start=1) if token == word]
            #in the line above we iterate through enumerated tokens of the text so as to take the indexes of the word
            document_info = [doc_id, word_frequency,positions]
            data.append({'word': word, 'DocumentInfo': document_info})

os.chdir('..') #so that we are in the main directory of the project
#every word used in the C.F. collection is stored at lexicon.txt file
# Create a DataFrame by concatenating the list of dictionaries
inverted_index = pd.DataFrame(data)

# Group and aggregate the DocumentInfo column
inverted_index = inverted_index.groupby('word')['DocumentInfo'].apply(list).reset_index()

# Save the DataFrame to a CSV file
inverted_index.to_csv('inverted_index.csv', index=False)