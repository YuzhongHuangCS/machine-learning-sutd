#!/bin/python
trainFileContent = [list(map(lambda i: float(i), line.split(','))) for line in open('train_1_5.csv', 'r')]
testFileContent = [list(map(lambda i: float(i), line.split(','))) for line in open('test_1_5.csv', 'r')]

initPara = [0.0, 0.0, 0.0]

def sign(row, para):
	return 1.0 if (para[0] * row[0] + para[1] * row[1] + para[2]) >= 0 else -1.0

def errors(para):
	return sum([sign((row[0], row[1]), para) != row[2] for row in trainFileContent])

def predictErrors(para):
	return sum([sign((row[0], row[1]), para) != row[2] for row in testFileContent])

def patch(para, row):
	return [
		para[0] + row[2] * row[0],
		para[1] + row[2] * row[1],
		para[2] + row[2]
	]

def analysys(para):
	for row in trainFileContent:
		if sign((row[0], row[1]), para) != row[2]:
			yield patch(para, row)

'''
@parameter: init para
@return: the best para among the child and sub-child para created by this para.
'''
def deepin(now, para, depth):
	if now < depth:
		results = [deepin(now+1, subPara, depth) for subPara in analysys(para)]

		thisErrors = [result[0] for result in results]
		thisPara = [result[1] for result in results]

		thisErrors.append(errors(para))
		thisPara.append(para)
	else:
		thisPara = list(analysys(para))
		thisPara.append(para)
		thisErrors = [errors(mPara) for mPara in thisPara]
		
	thisErrorMin = min(thisErrors)
	return (thisErrorMin, thisPara[thisErrors.index(thisErrorMin)])

finalResult = deepin(0, initPara, 1)
bestErrors = finalResult[0]
bestPara = finalResult[1]
predictionErrors = predictErrors(bestPara)

print("Best errors: %s, prediction errors: %s, best para: %s" % (bestErrors, predictionErrors, bestPara))
