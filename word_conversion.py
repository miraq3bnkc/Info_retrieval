"""In our C.F. collection we have many different variant forms for the same word.
   For example, we see the same numbers represented differently (eg. "52" and "fiftytwo") 
   So, in this script we are developing a function that converts words like "fiftytwo" to 
   their equivalent "52" """

from word2number import w2n
from num2words import num2words

def words_to_numbers(words):
    word_to_num = create_word_to_num_mapping()

    for i, word in enumerate(words):
        try:
            if word.lower()!="point":
                # Attempt conversion using word2number library
                # if word isnt "point" because it converts point to "0"
                numeric_value = str(w2n.word_to_num(word))
                words[i] = numeric_value  # Replace the original word at index i with its numeric value
        except ValueError:
            # If word2number fails, check direct mapping
            equivalent = word_to_num.get(word.lower())
            if equivalent is not None:
                words[i] = equivalent  # Replace the original word at index i with its equivalent
            else:
                # No direct mapping found, keep the original word
                pass

    return words  # Return the modified list of words


def create_word_to_num_mapping():
    word_to_num = {}

    for number in range(11, 100):  # Loop through numbers from 11 to 99
        word = num2words(number, lang='en')  # Convert number to words
        word = word.replace("-", "")  # Remove hyphens
        word_to_num[word] = str(number)  # Map the word to the number

    return word_to_num


#CHANGE REPRESENTATION OF "1ST" TO "first" etc. 
def replace_numerical_ordinals(words):
    for i, word in enumerate(words):
        if word[:-2].isdigit() and word[-2:].lower() in ['st', 'nd', 'rd', 'th']:
            print("in if",word)
            num = int(word[:-2])
            ordinal_word = num2words(num, ordinal=True)
            words[i] = ordinal_word

    return words