import numpy as np
import csv
import time
from sklearn.metrics import roc_auc_score

start_time = time.time() #starting chronometer

data = np.genfromtxt("Coll20012005small.csv" ,delimiter=",",dtype=int)
total_actors = list(set.union(set(data[:,0]),set(data[:,1])))
total_actors.sort()

print "Total unique actors = ", len(total_actors)
print "learning file loaded..."

binary_matrix = np.empty((len(total_actors),len(total_actors)),dtype=int)
for i in range(0,data.shape[0]): # fixed bug -1
    binary_matrix[total_actors.index(data[i,0]),total_actors.index(data[i,1])] = 1

print "binary matrix constructed..."

print binary_matrix

#finding out the common neighbors
neighbors = {}
for i in range(0,binary_matrix.shape[0]):
    neighbors[i] = np.array(np.where(binary_matrix[i,:]==1))

print "neighbors found..."

for i in range(0,binary_matrix.shape[0]):
    print "Common neighbors of ", i," are: ", neighbors[i]

number_of_neighbors = len(neighbors.keys())
print "Number of neighbors ", number_of_neighbors
score_matrix = np.empty((number_of_neighbors,number_of_neighbors),dtype=int)
for i in range(0,number_of_neighbors):
    for j in range(0,number_of_neighbors):
        score_matrix[i,j] = 0 if i==j else len(set(neighbors[i][0])&set(neighbors[j][0]))

print "score matrix computed ..."

print score_matrix

#load test data

#loading the test data
test = np.genfromtxt("AllColl20062007small.csv" ,delimiter=",",dtype=int)
test_list = [tuple(lst) for lst in test]

print test_list

scored_collaborations=[]
y_true= []
y_scores=[]
counter=0


for i in range(0,score_matrix.shape[0]):
    for j in range(0,score_matrix.shape[1]):
        t= (total_actors[i],total_actors[j])
        if i!=j and binary_matrix[i][j]!=1:
            #scored_collaborations.append([t, 1 if t in test_list else 0,score_matrix[i][j]])
            y_true.append(1 if t in test_list else 0)
            y_scores.append(score_matrix[i][j])
            #y_scores.append(1)
            counter +=1
            if (counter % 10000)==0:
                print "Inserted ", counter, " collaborations into y_true and y_score vectors"

#scored_collaborations= sorted(scored_collaborations, key=lambda x: x[2], reverse=True)

#print scored_collaborations

y_true=np.array(y_true)
y_scores=np.array(y_scores)

print roc_auc_score(y_true, y_scores)





quit()

#finding the top scores and its collaborators
top_scores = {}
scores =  list(np.unique(score_matrix))
#scores.remove(0) #removing zero because its predominant in number and can ease computation
for j in scores:
    top_scores[j] = np.where(score_matrix==j)


print "top scores and the collaborators indices found..."

print top_scores

#building the collaborators based on top scores
collaborations = []
scores.sort(reverse=True) #sorting the scores to get the top scores

print "neighbor scores : " , scores
#loading the test data
test = np.genfromtxt("test_col_matrix_toy" ,delimiter=",",dtype=int)

for i in scores:
    for j in range(0,len(top_scores[i][0])):
        if len(collaborations) <= len(total_actors)*(len(total_actors)-1):
            c = list ()
            c.append(total_actors[top_scores[i][0][j]])
            c.append(total_actors[top_scores[i][1][j]])
            collaborations.append(c)

print "collaborations built..."

print collaborations

training_list = [tuple(lst) for lst in collaborations]

print training_list



