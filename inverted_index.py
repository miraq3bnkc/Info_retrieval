import pandas as pd
from nltk.stem import SnowballStemmer
from word_conversion import words_to_numbers, replace_numerical_ordinals
from nltk.corpus import stopwords
import nltk


def generate_index_data(index,text,query):
    tokens = text.split() # split so as to get all the words
    tokens=  words_to_numbers(tokens)
    
    tokens = replace_numerical_ordinals(tokens)
    # Create a SnowballStemmer for English (Porter2)
    porter2 = SnowballStemmer('english')

    # Download NLTK stopwords 
    nltk.download('stopwords')
    # Get the list of English stop words
    stop_words = set(stopwords.words('english'))

    stemmed_tokens = [porter2.stem(token) for token in tokens if token.lower() not in stop_words]  # Stemming the tokens
    words=set(stemmed_tokens)  # Add words to the set , so as to not have duplicates
    data = []  # Create a list to store dictionaries for each word

    for word in words:  # Use a set to get unique words per document
        word_frequency = stemmed_tokens.count(word)
        if query==False:
            positions = [i for i, token in enumerate(stemmed_tokens,start=1) if token == word]
            #in the line above we iterate through enumerated tokens of the text so as to take the indexes of the word
            word_info = [index, word_frequency,positions] # Information per word in query
        else:
            #we arent trying to make a fully inverted index , so we will not save the positions this time
            word_info = [index, word_frequency] # Information per word in query
        
        data.append({'word': word, 'Information': word_info})

    return data


def generate_inverted_index(data,filemame):
    #Create a DataFrame by concatenating the list of dictionaries
    inverted_index = pd.DataFrame(data)

    # Group and aggregate the DocumentInfo column
    inverted_index = inverted_index.groupby('word')['Information'].apply(list).reset_index()

    # Save the DataFrame to a CSV file
    inverted_index.to_csv(filemame, index=False)