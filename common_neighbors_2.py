import numpy as np
import csv
import time

start_time = time.time()

def readdata(filename):
    return np.genfromtxt(filename ,delimiter=",",dtype=int)


def compute_neighbors(data,total_actors):

    binary_matrix = np.empty((len(total_actors),len(total_actors)),dtype=int)
    for i in range(0,data.shape[0]-1):
        binary_matrix[total_actors.index(data[i,0]),total_actors.index(data[i,1])] = 1    
    
    return binary_matrix


def find_common_neighbors(binary_matrix):
    neighbors = {}
    for i in range(0,binary_matrix.shape[0]):
        neighbors[i] = np.array(np.where(binary_matrix[i,:]==1))

    return neighbors



def get_score(neighbors):
    number_of_neighbors = len(neighbors.keys())
    score_matrix = np.empty((number_of_neighbors,number_of_neighbors),dtype=int)
    for i in range(0,number_of_neighbors):
        for j in range(0,number_of_neighbors):
            score_matrix[i,j] = 0 if i==j else len(set(neighbors[i][0])&set(neighbors[j][0]))

    return score_matrix



def find_top_scoring_neighbors(score_matrix):
    top_scores = {}
    scores =  list(np.unique(score_matrix))
    scores.remove(0) #removing zero because its predominant in number and can ease computation
    for j in scores:
        top_scores[j] = np.where(score_matrix==j)

    return top_scores


def build_collaborators(top_scores):
    collaborations = []
    scores.sort(reverse=True) #sorting the scores to get the top scores
    for i in scores:
        for j in range(0,len(top_scores[i][0])-1):
            if len(collaborations) <= 87433:
                c = list ()
                c.append(total_actors[top_scores[i][0][j]])
                c.append(total_actors[top_scores[i][1][j]])
                collaborations.append(c)
end




data = readdata("Collaborations20012005.csv")

test_data = readdata("NewCollaborations20062007.csv")

total_unique_actors = list(set.union(set(data[:,0]),set(data[:,1])))
total_unique_test_actors = list(set.union(set(data[:,0]),set(data[:,1]))) & list(set.union(set(test_data[:,0]),set(test_data[:,1])))

total_unique_actors.sort()

print "Total unique actors = ", len(total_actors)
print "learning file loaded..."

#constructing binary matrix based on collaborators
binary_matrix = compute_neighbors(data,total_unique_actors)
binary_matrix_for_test = compute_neighbors(test_data,total_unique_test_actors)

print "binary matrix constructed..."

#finding out the common neighbors

common_neighbors = find_common_neighbors(binary_matrix)


print "common neighbors found..."


#computing the score_matrix
print "computing score matrix..."

score_matrix = get_score(common_neighbors)


print "score matrix computed ..."


#finding the top scors and its collaborators
top_scores = find_top_scoring_neighbors(score_matrix)



print "top scores and the collaborators indices found..."

#building the collaborators based on top scores

collaborations = build_collaborators(top_scores)


print "collaborations built..."

#loading the test data
test = readdata("NewCollaborations20062007.csv")

training_list = [tuple(lst) for lst in collaborations]
test_list = [tuple(lst) for lst in test]

print "test set and collaborations coverted to proper format for evaluation"

#evaluation
correct = set(training_list) & set(test_list)


#accuracy 
print "Accuracy :", len(correct)/float(len(test))

print "Execution time = ", time.time() - start_time, " seconds"
