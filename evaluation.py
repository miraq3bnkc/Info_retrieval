"""
In this python file we will develop evaluation metrics for
the information retrieval and similarity calculations 
between the queries and the documents in the C.F. collection.

Information retrieval calculations we used Vector Space Model 
and ColBert. The rankings for each method are in "vsm_rankings.csv"
and "ranking.tsv" under the "experiments" directory accordingly.
For each method we ranked k=100 similar documents for every query.
"""

import math
from numpy import trapz
import pandas as pd
from find_and_change_ranking import find_files,  get_detailed_relevant_docs
import matplotlib.pyplot as plt

#PRECISION@K FUNCTION
def precision(retrieved,relevant,k):
    x=len(set(relevant).intersection(retrieved[:k]))
    return x/k

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

#CALCULATION OF NDCG (Normalization Discounted Cumulative Gain) EVALUATION METRIC
def ndcg(K,retrieved,numOfqueries,expert):
    experts=['Expert 1',"Expert 2","Expert 3","Expert 4"]
    detailed=get_detailed_relevant_docs()
    avg_dcg=0
    avg_idcg=0
    for query in range(numOfqueries):
        # Filter rows where "Query" column is equal to the current query
        filtered = detailed[detailed['Query'] == query].reset_index(drop=True) #in detailed the queries start from 0
        document_ids = filtered['Document_ID'].tolist()
        predicted=retrieved[query]

        dcg=0
        gains_list=[] #list of the gains in order we get the retrieved docs
        for k in range(1,K+1) :
            if str(predicted[k-1]) in document_ids:
                index=document_ids.index(str(predicted[k-1]))
                gain = int(filtered.loc[index,experts[expert-1]])
                discount=math.log2(1+k) #adding discount to the gain
            else:
                gain=0
            gains_list.append(gain)
            dcg=dcg+gain/discount #discounted cumulative gain

        idcg=0
        sorted_gains = sorted(gains_list, reverse=True)

        for i in range(1,K+1):
            if sorted_gains[i-1]>0 :
                #we only need to do these calculations for gain>0
                discount=math.log2(1+i) 
                idcg=idcg+sorted_gains[i-1]/discount #ideal discounted cumulative gain
        avg_dcg=avg_dcg+dcg/numOfqueries
        avg_idcg=avg_idcg+idcg/numOfqueries
    ndcg_score=avg_dcg/avg_idcg
    return ndcg_score

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

#get difference of two graphs
def area_difference(K, y1, y2):
    x=range(1,K+1)
    area1 = trapz(y1, x)
    area2 = trapz(y2, x)
    return area1 - area2


'''THIS IS WHERE THE MAIN CODE STARTS'''

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

map_colbert=[] #values for map y points
map_vsm=[] #values for map y points
ndcg_colbert=[]
ndcg_vsm=[] #list of lists for every experts y values

for K in range(1,101):
    map_colbert.append(mean_average_precision(K,retrieved_colbert,relevant))
    map_vsm.append(mean_average_precision(K,retrieved_vsm,relevant))

map_area=area_difference(100,map_colbert,map_vsm)
print("The MAP of Colbert is ",map_area,"different from VSM")

for expert in range (1,5):   
    ndcg_1=[]
    ndcg_2=[]
    for K in range(1,101):  
        colbert_ndcg=ndcg(K,retrieved_colbert,len(queries_relevant),expert)
        ndcg_1.append(colbert_ndcg)
        vsm_ndcg=ndcg(K,retrieved_vsm,len(queries_relevant),expert)
        ndcg_2.append(vsm_ndcg)

    ndcg_colbert.append(ndcg_1)
    ndcg_vsm.append(ndcg_2)

for j in range(0,4):
    ndcg_area=area_difference(100,ndcg_colbert[j],ndcg_vsm[j])
    print("The NDCG of Colbert is ",ndcg_area,"different from VSM (expert_",j+1,")")

#FROM THIS POINT ON WE ARE JUST CREATING PLOTS FOR EVERY METRIC WE USED 
    
x=[1]
x.extend(range(10,100,10))
x_axis=list(range(1,101))

plt.figure(1)
plt.plot(x_axis,map_colbert,c='hotpink',label='Colbert')
plt.plot(x_axis,map_vsm,c='#4CAF50',label='VSM')
plt.xticks(range(0,100,10), x)
leg = plt.legend(loc='upper left')

plt.ylabel("Mean Average Precision")
plt.xlabel("K items returned")

plt.figure(2)
plt.plot(x_axis,ndcg_colbert[0],c='magenta',label='Colbert')
plt.plot(x_axis,ndcg_vsm[0],c='blue',label='VSM')
plt.xticks(range(0,100,10), x)
leg = plt.legend(loc='upper right')

plt.ylabel("Normalized Discounted Cumulative Gain")
plt.xlabel("K items returned")
plt.title('Relevance score by REW')

plt.figure(3)
plt.plot(x_axis,ndcg_colbert[1],c='magenta',label='Colbert')
plt.plot(x_axis,ndcg_vsm[1],c='blue',label='VSM')
plt.xticks(range(0,100,10), x)
leg = plt.legend(loc='upper right')

plt.ylabel("Normalized Discounted Cumulative Gain")
plt.xlabel("K items returned")
plt.title('Relevance score by REW colleagues')

plt.figure(4)
plt.plot(x_axis,ndcg_colbert[2],c='magenta',label='Colbert')
plt.plot(x_axis,ndcg_vsm[2],c='blue',label='VSM')
plt.xticks(range(0,100,10), x)
leg = plt.legend(loc='upper right')

plt.ylabel("Normalized Discounted Cumulative Gain")
plt.xlabel("K items returned")
plt.title('Relevance score by REW post-doctorates')

plt.figure(5)
plt.plot(x_axis,ndcg_colbert[1],c='magenta',label='Colbert')
plt.plot(x_axis,ndcg_vsm[1],c='blue',label='VSM')
plt.xticks(range(0,100,10), x)
leg = plt.legend(loc='upper right')

plt.ylabel("Normalized Discounted Cumulative Gain")
plt.xlabel("K items returned")
plt.title('Relevance score by JBW')

plt.show()

#ALL GRAPHS EXIST IN DIRECTORY 'graph_figures/'