import numpy as np
import csv
import time
import sys

from sklearn.metrics import roc_auc_score

#user-defined module
import common_methods as cm

#starting chronometer
start_time = time.time() 

print "Program stated : " , start_time


#read training data
data = cm.readdata(sys.argv[1])


#get sorted list of total number unique actors present in training data
total_actors = cm.total_actors_with_sort(data)


print "Total unique actors = ", len(total_actors)
print "learning file loaded..."


#construct binary matrix from traning data
binary_matrix = cm.construct_binary_matrix(data,total_actors)



print "binary matrix constructed..."

print binary_matrix

#finding out the common neighbors
neighbors = cm.compute_common_neighbors(binary_matrix)


 
print "neighbors found..."


cm.print_common_neighbors(binary_matrix,neighbors)


#compute score matrix of all possible neighbors
score_matrix = cm.compute_score_matrix(neighbors)



print "score matrix computed ..."

print score_matrix

#load test data

#loading the test data
test_data = cm.readdata(sys.argv[2])

#represting test set as a list of sets
test_list = [tuple(lst) for lst in test_data]

print test_list

scored_collaborations=[]
y_true= []
y_scores=[]
counter=0

threshold=1

#building path name to store the blocked collaborations
path_names = sys.argv[1].split('/')
complete_path = '/'.join(path_names[:-1])+'block'+str(threshold)+path_names[-1]


# blockfn=''

# for i in range(0,len(sp)-1):
#     blockfn+= sp[i]+'/'

# blockfn+= 'block'+str(threshold)+sp[len(sp)-1]
# print blockfn



#writing the blocked collaborations
f = open(complete_path,'w')


for i in range(0,score_matrix.shape[0]):
    for j in range(0,score_matrix.shape[1]):
        if i!=j and binary_matrix[i][j]!=1 and score_matrix[i][j]>=threshold:
            f.write(str(total_actors[i])+'\t'+str(total_actors[j])+'\n')
f.close()

#print scored_collaborations



quit()

#finding the top scores and its collaborators
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



