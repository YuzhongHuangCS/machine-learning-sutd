#!/bin/python3
import copy
import math

trainFile = open('train_1_5.csv', 'r')
testFile = open('test_1_5.csv', 'r')

trainFileContent = [list(map(lambda i: float(i), line.split(','))) for line in trainFile]
testFileContent = [list(map(lambda i: float(i), line.split(','))) for line in testFile]

initPara = [0, 0, 0]

def sign(point, para):
	return math.copysign(1, (para[0] * point[0] + para[1] * point[1] + para[2]))

def errors(para):
	return sum([int(sign((row[0], row[1]), para) != row[2]) for row in trainFileContent])

def predictErrors(para):
	return sum([int(sign((row[0], row[1]), para) != row[2]) for row in testFileContent])

def patch(para, data):
	tryPara = copy.deepcopy(para)
	tryPara[0] += data[2] * data[0]
	tryPara[1] += data[2] * data[1]
	tryPara[2] += data[2]

	return tryPara

def analysys(para):
	for row in trainFileContent:
		if sign((row[0], row[1]), para) != row[2]:
			yield patch(para, row)

'''
@parameter: init para
@return: the best para among the child and sub-child para created by this para.
'''
def deepin(i, para, depth):
	if i < depth:
		tryPara = list(analysys(para))
		results = [deepin(i+1, subPara, depth) for subPara in tryPara]

		thisErrors = [result[0] for result in results]
		thisPara = [result[1] for result in results]

		thisErrors.append(errors(para))
		thisPara.append(para)

	else:
		thisPara = list(analysys(para))
		thisPara.append(para)
		thisErrors = [errors(para) for para in thisPara]
		
	thisErrorMin = min(thisErrors)
	return(thisErrorMin, thisPara[thisErrors.index(thisErrorMin)])

finalResult = deepin(0, initPara, 1)
bestErrors = finalResult[0]
bestPara = finalResult[1]
predictionError = predictErrors(bestPara)

print(bestErrors)
print(bestPara)
print(predictionError)
