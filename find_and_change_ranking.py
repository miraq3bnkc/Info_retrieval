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


#this function processes "cfquery_detailed" and we take relevant docs for each query and its scores (experts)
def get_detailed_relevant_docs():
    with open("cfquery_detailed") as file:
        data=file.read()

    # Initialize empty lists to store data
    query_list = []
    doc_id = []
    expert_1 = []
    expert_2 = []
    expert_3 = []
    expert_4 = []

    docs_and_experts=[]

    while True:
        # Find the index of "RD"
        x = data.find("RD")
        if x == -1:
            break 

        # Find the index of "QN" starting from the position of "RD"
        y = data.find("QN", x)
        if y == -1:
            # Extract the text between "RD" and EOF
            docs_and_experts.append( data[x + len("RD"):].split())
            break  # Break the loop if "QN" is not found

        # Extract the text between "RD" and "QN"
        docs_and_experts.append( data[x + len("RD"):y].split())
        # Update data to remove the processed part
        data = data[y + len("QN"):]

    for index,list in enumerate(docs_and_experts):
        for i,_ in enumerate(list):
            if i%2!=0 :
                experts=list[i]
                expert_1.append(experts[0])
                expert_2.append(experts[1])
                expert_3.append(experts[2])
                expert_4.append(experts[3])
            else:
                doc_id.append(list[i])
            if i + 1 <= len(list)/2:
                query_list.append(index)


    #convert into dataframe
    data = {'Query': [], 'Document_ID': [], 'Expert 1': [], 'Expert 2': [], 'Expert 3': [], 'Expert 4': []}
    data['Query']=query_list
    data['Document_ID']=doc_id
    data['Expert 1']=expert_1
    data['Expert 2']=expert_2
    data['Expert 3']=expert_3
    data['Expert 4']=expert_4

    return pd.DataFrame(data)