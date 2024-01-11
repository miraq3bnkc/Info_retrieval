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

def recall(retrieved,relevant,k):
    x=len(relevant.intersection(retrieved[:k]))
    y=len(relevant)
    return x/y

def precision(retrieved,relevant,k):
    x=len(relevant.intersection(retrieved[:k]))
    return x/k

def average_precision(K,retrieved,relevant):
    sum=0
    for k in K:
        sum= sum + precision(retrieved,relevant,k)
    AP=sum / len(relevant)
    return AP


colbert_rank=pd.read_csv(find_files("ranking.tsv"))
vsm_rank=pd.read_csv("vsm_rankings.csv")

#load relevant documents from file "Relevant_20"
with open("Relevant_20") as f:
    queries_relevant=f.readlines()
#list of relevant documents in a list for each query (list of lists)
relevant = [line.strip().split() for line in queries_relevant]



#RECALL FUNCTION 