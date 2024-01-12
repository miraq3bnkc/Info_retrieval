"""
In this python file we will develop evaluation metrics for
the information retrieval and similarity calculations 
between the queries and the documents in the C.F. collection.

Information retrieval calculations we used Vector Space Model 
and ColBert. The rankings for each method are in "vsm_rankings.csv"
and "ranking.tsv" under the "experiments" directory accordingly.
For each method we ranked k=100 similar documents for every query.
"""

import pandas as pd
from find_and_change_ranking import find_files
import matplotlib.pyplot as plt
import numpy as np

#RECALL@K FUNCTION
def recall(retrieved,relevant,k):
    x=len(set(relevant).intersection(retrieved[:k]))
    y=len(relevant)
    return x/y

#PRECISION@K FUNCTION
def precision(retrieved,relevant,k):
    x=len(set(relevant).intersection(retrieved[:k]))
    return x/k

def recall_precision_graph():
    #lets just look for it on the book later
    return 0

#CALCULATION OF MAP (MEAN AVERAGE PRECISION) EVALUATION METRIC
def mean_average_precision(K,retrieved,relevant):
    big_sum=0
    for query in range(20):
        predicted=retrieved[query]
        actual=relevant[query]
        sum=0
        for k in range(K):
            if predicted[k] in actual:
                rel=1
            else:
                rel=0
            mul=precision(predicted,actual,k+1)*rel
            sum= sum + mul
        AP=sum / len(relevant)
        big_sum=big_sum+AP
    mean_average_precision=big_sum/20
    return mean_average_precision

def get_retrieved_docs(dataframe):
    # Create an empty dictionary to store results
    result_list = []

    # Iterate over each query
    for query in range(20):

        # Filter rows where "Query" column is equal to the current query
        filtered_df = dataframe[dataframe['Query'] == query+1]

        # Extract values from "Document_ID" column and store in a list
        document_ids_list = filtered_df['Document_ID'].tolist()

        # Append the list to the result_list
        result_list.append(document_ids_list)
    return result_list


colbert_rank=pd.read_csv(find_files("ranking.tsv"),delimiter='\t')
vsm_rank=pd.read_csv("vsm_rankings.csv")

#load relevant documents from file "Relevant_20"
with open("Relevant_20") as f:
    queries_relevant=f.readlines()
#list of relevant documents in a list for each query (list of lists)
relevant = [list(map(int,line.strip().split())) for line in queries_relevant] #every doc name is stored as int


#list of retrieved documents for each query (list of lists)
retrieved_colbert=get_retrieved_docs(colbert_rank)
retrieved_vsm=get_retrieved_docs(vsm_rank)

map_colbert=mean_average_precision(100,retrieved_colbert,relevant)
print(map_colbert)

map_vsm=mean_average_precision(100,retrieved_vsm,relevant)
print(map_vsm)