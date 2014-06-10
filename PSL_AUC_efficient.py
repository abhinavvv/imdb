import numpy as np
import csv
import time
import sys
import common_methods as cm
from sklearn.metrics import roc_auc_score

start_time = time.time() #starting chronometer



#loading training and test data
data = cm.readdata(sys.argv[1])
test_data = cm.readdata(sys.argv[2])


#getting total actors from collaborations
total_actors = cm.total_actors_with_sort(data)


print "Total unique actors = ", len(total_actors)
print "learning file loaded..."


#constructing binary matrix for training and test set

binary_matrix = cm.construct_binary_matrix(data,total_actors)

test_binary_matrix = cm.construct_binary_matrix(test_data,total_actors)




print "binary matrix constructed..."

print binary_matrix

#finding out the common neighbors
neighbors = cm.compute_common_neighbors(binary_matrix)


print "neighbors found..."

#printing out common neighbors...
cm.print_common_neighbors(binary_matrix,neighbors)


#constructing PSL output based score matrix...
number_of_neighbors = len(neighbors.keys())
print "Number of neighbors ", number_of_neighbors
score_matrix = np.zeros((number_of_neighbors,number_of_neighbors),dtype=float)
    

with open(sys.argv[3]) as csvfile:
    row = csv.reader(csvfile)
    for value in row:
        score_matrix[total_actors.index(int(value[0].split('(')[1])), 
            total_actors.index(int(value[1].split(')')[0]))] = float(value[1].split(')')[1])


print "score matrix computed ..."

print score_matrix


#compute AUC parameters...
y_true, y_scores = cm.compute_auc_params(score_matrix, binary_matrix, test_binary_matrix)
#compute AUC
print roc_auc_score(y_true, y_scores)
