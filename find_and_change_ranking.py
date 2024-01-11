import os
import pandas as pd 
  
def change(filename):
    # read contents of tsv file 
    file = pd.read_csv(filename, delimiter='\t', header=None) 

     # Get a list of filenames in the 'docs/' directory
    docs_filenames = sorted(os.listdir('docs/'))

    # Replace 'Document_ID' values with corresponding filenames
    file.iloc[:,1] = [docs_filenames[i] for i in file.iloc[:,1]]

    # Create a new DataFrame with the header and updated column values
    new_file = pd.DataFrame(file.values, columns=['Query', 'Document_ID', 'Rank', 'Similarity'])

    # converting data frame to tsv and updating the existing file
    new_file.to_csv(filename, sep='\t', index=False)  
  

def has_expected_header(filename):
    filename = pd.read_csv(filename, delimiter='\t') 
    if 'Query' in filename:
       return True
    else:
       return False


def find_files(filename):
    # Walking top-down from the root
    for root, dir, files in os.walk('experiments/notebook/using_colbert'):
        if filename in files:
            full_path=os.path.join(root, filename)
            if not has_expected_header(full_path):
                change(full_path)
            return full_path
