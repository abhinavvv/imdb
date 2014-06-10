import sys
import csv
import random



def readdata():
	data=[]
	with open(sys.argv[1], 'r') as file:
		reader = csv.reader(file, delimiter=',')
		for row in reader:
			data.append(tuple(row))
	return data


def writedata(filename,data):
	file = open(filename, 'w')
	wr = csv.writer(file, delimiter='\t')
	wr.writerows(data)





data = readdata()
print "data read..."
train_data = random.sample(set(data),int(0.7*len(data)))
test_data = list(set(data) - set(train_data))

print "train and test data constructed"

train_data_filename = sys.argv[1].split('.')[0] + "_train.tsv"
test_data_filname = sys.argv[1].split('.')[0] + "_test.tsv"

print " File names with location for train and test are : ", train_data_filename, test_data_filname

writedata(train_data_filename,train_data)
writedata(test_data_filname,test_data)
