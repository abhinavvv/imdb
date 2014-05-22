#give input in the following way - training_file_name test_file_name output_file_name
#eg python common_neighbors.py train.csv test.csv output.csv

import numpy as np
import sys
import csv

#training pahse

#uploading training_data
data = np.genfromtxt(sys.argv[1],delimiter=",",dtype=int)

#calculating the neighbors for each actor
neighbors = {}
for i in range(0,data.shape[0]):
    neighbors[i] = np.array(np.where(data[i,:]==1))
number_of_neighbors = len(n.keys())

#logic for calculating score_matrix
score_matrix = np.empty((number_of_neighbors,number_of_neighbors),dtype=int)
for i in range(0,number_of_neighbors):
    for j in range(0,number_of_neighbors):
        score_matrix[i,j] = 0 if i==j else len(set(neighbors[i][0])&set(neighbors[j][0]))
        #could do a better implementation where you can have another condition
        #stating that if i > j then score_matrix[j,i] = score_matrix[i,j]
        

#prediction phase

#test data loaded
test_data = np.genfromtxt(sys.argv[2],delimiter=",",dtype=int)

#test_matrix has the result of prediction
test_matrix = np.empty((test_data.shape[0],test_data.shape[1]),dtype=int)

#finding a threshold based on average of actor(i)
for i in range(0,test_data.shape[0]):
    for j in range(0,test_data.shape[1]):
            test_matrix[i,j] = 1 if score_matrix[i,j] >= sum(score_matrix[i,:])/len(score_matrix[i,:]) else 0


#evaluating the predicted values
result = test_data == test_matrix

#a matrix for evaluating the results.
result_matrix = np.zeros((result.shape[0],result.shape[1]),dtype=int)
for i in range(0,result.shape[0]):
    for j in range(0,result.shape[1]):
        result_matrix[i,j] = 0 if result[i,j] else 1


#results

#exporting result to csv 
csvfile = file(sys.argv[3], 'wb')
writer = csv.writer(csvfile)
writer.writerows(result_matrix)
csvfile.close()