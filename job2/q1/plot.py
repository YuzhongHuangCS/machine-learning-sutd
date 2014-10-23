#!/bin/python
from numpy import *
import matplotlib.pyplot as plt

trainFile = array([list(map(lambda i: float(i), line.split(','))) for line in open('train_warfarin.csv', 'r')])
validationFile = array([list(map(lambda i: float(i), line.split(','))) for line in open('validation_warfarin.csv', 'r')])
testFile = array([list(map(lambda i: float(i), line.split(','))) for line in open('test_warfarin.csv', 'r')])

draw = {}
draw['train'] = []
draw['validation'] = []
draw['test'] = []

def cost(w, b, dataSet, labelSet):
	return average((labelSet - dot(w, dataSet) - b) ** 2)

def fileCost(w, b, file):
	return cost(w, b, file[:, 1:].transpose(), file[:, 0].transpose())

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

		draw['train'].append(fileCost(initW, initB, trainFile))
		draw['validation'].append(fileCost(initW, initB, validationFile))
		draw['test'].append(fileCost(initW, initB, testFile))

	return {
		"w": initW,
		"b": initB,
		"cost": cost(initW, initB, dataSet, labelSet)
	}

bestRate = 0.21
bestResult = analysys(trainFile, bestRate)

plt.plot(range(100), draw['train'], linewidth = 2, label = 'train')
plt.plot(range(100), draw['validation'], linewidth = 2, label = 'validation')
plt.plot(range(100), draw['test'], linewidth = 2, label = 'test')
plt.show()