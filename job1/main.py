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

globalPara = []
globalErrors = []

def deepin(i, para, limit):
	refinedPara = list(analysys(para))
	refinedPara.append(para)

	refinedErrors = [errors(para) for para in refinedPara]
	refinedErrorMin = min(refinedErrors)


for roughPara in analysys(initPara):
	refinedPara = list(analysys(roughPara))
	refinedPara.append(roughPara)

	refinedErrors = [errors(para) for para in refinedPara]
	refinedErrorMin = min(refinedErrors)

	globalErrors.append(refinedErrorMin)
	globalPara.append(refinedPara[refinedErrors.index(refinedErrorMin)])

globalPara.append(initPara)
globalErrors.append(errors(initPara))

#print(globalPara)
#print(globalErrors)

bestErrors = min(globalErrors)
bestPara = globalPara[globalErrors.index(bestErrors)]
predictionError = predictErrors(bestPara)

print(bestErrors)
print(bestPara)
print(predictionError)