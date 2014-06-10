import sys
import numpy as np
import csv
import time

from sklearn.metrics import roc_auc_score

#user-defined module
import common_methods as cm

start_time = time.time() #starting chronometer

#read training data
data = cm.readdata(sys.argv[1])


#get sorted list of total number unique actors present in training data
total_actors = cm.total_actors_with_sort(data)


print "Total unique actors = ", len(total_actors)
print "learning file loaded..."

#compute binary matrix for training data
binary_matrix = cm.construct_binary_matrix(data,total_actors)


print "binary matrix constructed..."


print binary_matrix

#finding out the common neighbors
neighbors = cm.compute_common_neighbors(binary_matrix)



print "neighbors found..."

#printing common neighbors
cm.print_common_neighbors(binary_matrix,neighbors)



#compute score matrix
score_matrix = cm.compute_score_matrix(neighbors)


print "score matrix computed ..."

print score_matrix

#load test data

#loading the test data
test_data = cm.readdata(sys.argv[2])

test_binary_matrix = cm.construct_binary_matrix(test_data,total_actors)
#representing test data as a list of set
test_list = [tuple(lst) for lst in test_data]

print test_list

scored_collaborations=[]
y_true= []
y_scores=[]
counter=0

print "computing AUC..."

#computing AUC parameters, true values and scores of them.
y_true, y_scores = cm.compute_auc_params(score_matrix, binary_matrix, test_binary_matrix)


#compute auc
print roc_auc_score(y_true, y_scores)


