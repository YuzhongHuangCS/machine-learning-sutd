#!/usr/bin/pypy
import math

trainSet = [list(map(lambda i: float(i), line.split(' '))) for line in open('trainfeat.txt', 'r')]
trainLabel = [float(line) for line in open('trainlabs.txt', 'r')]
#testSet = [list(map(lambda i: float(i), line.split(' '))) for line in open('testfeat.txt', 'r')]
#testLabel = [float(line) for line in open('testlabs.txt', 'r')]

features = len(trainSet[0])
samples = len(trainSet)
total = len(trainLabel)
totalTrue = sum(trainLabel)

def prepare(data):
	table = []
	for f in range(features):
		table.append({})
		for r in range(samples):
			if table[f].get(data[r][f]) == None:
				table[f][data[r][f]] = 1
			else:
				table[f][data[r][f]] += 1
	return table

def prepareTrue(data, label):
	table = []
	for f in range(features):
		table.append({})
		for r in range(samples):
			if table[f].get(data[r][f]) == None:
				table[f][data[r][f]] = 0
			if label[r] == 1:
				table[f][data[r][f]] += 1
	return table

def entropy(first, second):
	try:
		total = first + second
		fp = float(first) / total
		sp = float(second) / total
		return -((fp * math.log(fp, 2)) + (sp * math.log(sp, 2)))
	except ValueError as e:
		if (first == 0) or (second == 0):
			return -math.log(1, 2)
		else:
			raise e

def indexEntropy2(index, table):
	sums = sum([table[index][item] for item in table[index]])

	def merge(item):
		p = float(table[index][item]) / sums
		return p * math.log(p, 2)

	info = [merge(item) for item in table[index]]

	return -sum(info)

def expectEntropy(index, table):
	choices = len(table[index])


class Node(object):
	def __init__(self, labelIndex, entropy, features, samples):
		super(Node, self).__init__()
		self.labelIndex = labelIndex
		self.entropy = entropy
		self.features = features
		self.samples = samples

		
trainTable = prepare(trainSet)
trainTrueTable = prepareTrue(trainSet, trainLabel)
initEntropy = entropy(totalTrue, total-totalTrue)
print initEntropy

def indexEntropy(index):
	thisResult = []
	for key, value in trainTable[index].items():
		trueValue = trainTrueTable[index][key]
		newEntropy = entropy(value - trueValue, trueValue)
		thisResult.append((newEntropy, value))
	
	aggr = 0
	weightSum = 0
	for item in thisResult:
		weightSum += item[1]
		aggr += item[0] * item[1]
	return aggr / weightSum

candidateEntropy = [indexEntropy(index) for index in range(features)]
maxEntropy = min(candidateEntropy)
print candidateEntropy, maxEntropy, candidateEntropy.index(maxEntropy)
RootNode = Node(candidateEntropy.index(maxEntropy))