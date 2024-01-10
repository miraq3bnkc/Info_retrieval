"""
In this python file we will develop evaluation metrics for
the information retrieval and similarity calculations 
between the queries and the documents in the C.F. collection.

Information retrieval calculations we used Vector Space Model 
and ColBert. The rankings for each method are in "vsm_rankings.csv" and 
"experiments/notebook/using_colbert/2024-01/06/20.14.26/ranking.tsv"
accordingly. For each method we ranked k=100 similar documents for 
every query.
"""

import pandas as pd

def recall(retrieved,relevant):
    x=len(relevant.intersection(retrieved))
    y=len(relevant)
    return x/y

def precision(retrieved,relevant):
    x=len(relevant.intersection(retrieved))
    y=len(retrieved)
    return x/y

colbert_rank=pd.read_csv("experiments/notebook/using_colbert/2024-01/06/20.14.26/ranking.tsv", delimiter='\t')
vsm_rank=pd.read_csv("vsm_rankings.csv")

#load relevant documents from file "Relevant_20"
with open("Relevant_20") as f:
    queries_relevant=f.readlines()
#list of relevant documents in a list for each query (list of lists)
relevant = [queries_relevant.strip().split() for line in queries_relevant]



#RECALL FUNCTION 