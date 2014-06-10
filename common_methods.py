import numpy as np

def readdata(filename):
	data = np.genfromtxt(filename ,delimiter=",",dtype=int)
	return data

def total_actors_with_sort(data):
	total_actors = list(set.union(set(data[:,0]),set(data[:,1])))
	total_actors.sort()
	return total_actors

def construct_binary_matrix(data,total_actors):
	binary_matrix = np.empty((len(total_actors),len(total_actors)),dtype=int)
	for i in range(0,data.shape[0]):
		binary_matrix[total_actors.index(data[i,0]),total_actors.index(data[i,1])] = 1

	return binary_matrix

def compute_common_neighbors(binary_matrix):
	neighbors = {}
	for i in range(0,binary_matrix.shape[0]):
		neighbors[i] = np.array(np.where(binary_matrix[i,:]==1))

	return neighbors

def print_common_neighbors(binary_matrix,neighbors):
	for i in range(0,binary_matrix.shape[0]):
		print "Common neighbors of ", i," are: ", neighbors[i]


def compute_score_matrix(neighbors):
	number_of_neighbors = len(neighbors.keys())
	print "Number of neighbors ", number_of_neighbors
	score_matrix = np.empty((number_of_neighbors,number_of_neighbors),dtype=int)
	for i in range(0,number_of_neighbors):
		for j in range(0,number_of_neighbors):
			score_matrix[i,j] = 0 if i==j else len(set(neighbors[i][0])&set(neighbors[j][0]))

	return score_matrix

def compute_auc_params(score_matrix,binary_matrix,test_binary_matrix):
	scored_collaborations=[]
	y_true= []
	y_scores=[]
	counter=0
	for i in range(0,score_matrix.shape[0]):
		for j in range(0,score_matrix.shape[1]):
			if i!=j and binary_matrix[i][j]!=1:
				y_true.append(1 if test_binary_matrix[i][j]==1 else 0)
				y_scores.append(score_matrix[i][j])
            	counter +=1
            	if (counter % 10000)==0:
            		print "Inserted ", counter, " collaborations into y_true and y_score vectors"
	
	y_true = np.array(y_true)
	y_scores = np.array(y_scores)
	return (y_true,y_scores)

