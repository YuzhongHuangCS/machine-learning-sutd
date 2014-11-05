#!/bin/python
from numpy import *

trainFile = array([list(map(lambda i: float(i), line.split(','))) for line in open('train_warfarin.csv', 'r')])
validationFile = array([list(map(lambda i: float(i), line.split(','))) for line in open('validation_warfarin.csv', 'r')])
testFile = array([list(map(lambda i: float(i), line.split(','))) for line in open('test_warfarin.csv', 'r')])

def cost(w, b, dataSet, labelSet):
	return average((labelSet - dot(w, dataSet) - b) ** 2)

def fileCost(file, result):
	return cost(result['w'], result['b'], file[:, 1:].transpose(), file[:, 0].transpose())

def analysys(file, rate):
	dataSet = file[:, 1:].transpose()
	labelSet = file[:, 0].transpose()
	initW = empty(dataSet.shape[0])
	initB = 0

	for count in range(100):
		half = labelSet - dot(initW, dataSet) - initB
		meta = dot(dataSet, half) / dataSet.shape[1] * 2 * rate

		initW += meta
		initB += average(half) * 2 * rate

	return {
		"w": initW,
		"b": initB,
		"cost": cost(initW, initB, dataSet, labelSet)
	}

def frange(start, stop, step):
	while start < stop:
		yield start
		start += step

bestRate = 0.01
bestResult = analysys(trainFile, bestRate)

for rate in frange(0.01, 0.25, 0.01):
	result = analysys(trainFile, rate)
	if fileCost(validationFile, result) < fileCost(validationFile, bestResult):
		bestResult = result
		bestRate = rate

print("Best learning rate: %s" % bestRate)
print("Trainning set error: %s" % bestResult['cost'])
print("Validation set error: %s" % fileCost(validationFile, bestResult))
print("Test set error: %s" % fileCost(testFile, bestResult))
