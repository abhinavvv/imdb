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





quit()

# #finding the top scores and its collaborators
# top_scores = {}
# scores =  list(np.unique(score_matrix))
# #scores.remove(0) #removing zero because its predominant in number and can ease computation
# for j in scores:
#     top_scores[j] = np.where(score_matrix==j)


# print "top scores and the collaborators indices found..."

# print top_scores

# #building the collaborators based on top scores
# collaborations = []
# scores.sort(reverse=True) #sorting the scores to get the top scores

# print "neighbor scores : " , scores
# #loading the test data
# test = np.genfromtxt("test_col_matrix_toy" ,delimiter=",",dtype=int)

# for i in scores:
#     for j in range(0,len(top_scores[i][0])):
#         if len(collaborations) <= len(total_actors)*(len(total_actors)-1):
#             c = list ()
#             c.append(total_actors[top_scores[i][0][j]])
#             c.append(total_actors[top_scores[i][1][j]])
#             collaborations.append(c)

# print "collaborations built..."

# print collaborations

# training_list = [tuple(lst) for lst in collaborations]

# print training_list



