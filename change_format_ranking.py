import os
import pandas as pd 

def insert_header(file_path, header):
    # Read the existing content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Insert the new header line at the beginning of the content
    lines.insert(0, header)

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

  
def change(filename):
    # read contents of tsv file 
    file = pd.read_csv(filename, delimiter='\t', header=None) 
    # adding header 
    headerLine = 'Query\tDocument_ID\tRank\tSimilarity\n' 
    insert_header(filename,headerLine)

     # Get a list of filenames in the 'docs/' directory
    docs_filenames = sorted(os.listdir('docs/'))

    # Replace 'Document_ID' values with corresponding filenames
    file.iloc[:,1] = [docs_filenames[i] for i in file.iloc[:,1]]

    # converting data frame to tsv and updating the existing file
    file.to_csv(filename, sep='\t', index=False)  
  

def find_files(filename):
   # Walking top-down from the root
   for root, dir, files in os.walk('experiments/notebook/using_colbert'):
      if filename in files:
         name=os.path.join(root, filename)
         change(name)

find_files('ranking.tsv')