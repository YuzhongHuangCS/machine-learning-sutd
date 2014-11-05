#!/usr/bin/pypy
import math
import heapq
import copy
import random
import json

# Prepare Data
trainSet = [list(map(lambda i: float(i), line.split(' '))) for line in open('trainfeat.txt', 'r')]
trainLabel = [float(line) for line in open('trainlabs.txt', 'r')]
testSet = [list(map(lambda i: float(i), line.split(' '))) for line in open('testfeat.txt', 'r')]
testLabel = [float(line) for line in open('testlabs.txt', 'r')]

dataPack = zip(trainSet, trainLabel)
random.shuffle(dataPack)
trainPack = dataPack[5000:]
validationPack = dataPack[:5000]

trainSet, trainLabel = zip(*trainPack)
validationSet, validationLabel = zip(*validationPack)

trainSet = list(trainSet)
trainLabel = list(trainLabel)
validationSet = list(validationSet)
validationLabel = list(validationLabel)

def entropy(first, second):
	if (first == 0) or (second == 0):
		return -math.log(1, 2)

	fp = float(first) / (first + second)
	sp = 1 - fp
	return -((fp * math.log(fp, 2)) + (sp * math.log(sp, 2)))

class Node(object):
	def __init__(self, data, label, feature, featureIndex = None, featureValue = None, flag = None):
		super(Node, self).__init__()
		self.data = data
		self.label = label
		self.feature = feature
		self.featureIndex = featureIndex
		self.featureValue = featureValue
		self.flag = flag
		self.childs = {}
		
		if flag == None:
			self.features = len(data[0])
			self.samples = len(data)
			self.trues = int(sum(label))
			#self.entropy = entropy(self.trues, self.samples - self.trues)

			#print("Sample: %s, Feature: %s, Trues: %s, FeatureIndex: %s, FeatureValue: %s" % (self.samples, self.features, self.trues, self.featureIndex, self.featureValue))
			if self.samples > 1 and self.features > 1 and self.trues != 0 and self.trues != self.samples:
				self.prepare()
				self.prepareTrue()
				self.grow()
			else:
				if self.samples >= (2 * self.trues):
					self.flag = False
				else:
					self.flag = True

		else:
			pass
			#print("FeatureIndex: %s, FeatureValue: %s, Flag: %s" % (self.featureIndex, self.featureValue, self.flag))

		del self.data
		del self.label
		del self.feature

	def prepare(self):
		table = []

		for f in range(self.features):
			table.append({})
			for r in range(self.samples):
				if table[f].get(self.data[r][f]) == None:
					table[f][self.data[r][f]] = 1
				else:
					table[f][self.data[r][f]] += 1

		self.table = table

	def prepareTrue(self):
		table = []

		for f in range(self.features):
			table.append({})
			for r in range(self.samples):
				if table[f].get(self.data[r][f]) == None:
					table[f][self.data[r][f]] = 0
				if self.label[r] == 1:
					table[f][self.data[r][f]] += 1

		self.trueTable = table

	def indexToEntropy(self, index):
		aggregate = 0.0
		weightSum = 0.0

		for key, value in self.table[index].items():
			trueValue = self.trueTable[index][key]
			newEntropy = entropy(value - trueValue, trueValue)
			aggregate += newEntropy * value
			weightSum += value

		return aggregate / weightSum

	def grow(self):
		'''
		key -> globalFeatureIndex
		index -> localFeatureIndex
		'''

		candidates = []
		localFeatureIndex = 0

		for key, value in self.feature.items():
			if value == False:
				continue
			else:
				heapq.heappush(candidates, (self.indexToEntropy(localFeatureIndex), localFeatureIndex, key))
				localFeatureIndex += 1

		choice = heapq.heappop(candidates)
		self.ruleIndex = choice[2]
		index = choice[1]

		#print(choice)
		#print(self.table[index])
		#print(self.trueTable[index])
		#print(self.entropy, choice[0])

		childFeature = copy.deepcopy(self.feature)
		childFeature[choice[2]] = False

		if len(self.table[index]) == 1:
			key, value = self.table[index].popitem()
			key, trueValue = self.trueTable[index].popitem()
			if value >= (2 * trueValue):
				childNode = Node(None, None, childFeature, choice[2], key, False)
			else:
				childNode = Node(None, None, childFeature, choice[2], key, True)

			self.childs[key] = childNode
			return

		for key in self.table[index]:
			childData = copy.deepcopy(self.data)
			childLabel = copy.deepcopy(self.label)

			i = 0
			while i < len(childData):
				if childData[i][index] != key:
					del childData[i]
					del childLabel[i]
				else:
					del childData[i][index]
					i += 1

			childNode = Node(childData, childLabel, childFeature, choice[2], key)
			self.childs[key] = childNode

	def query(self, data):
		if self.flag == None:
			key = data[self.ruleIndex]
			#print key

			child =  self.childs.get(key)
			if child == None:
				trys = [tryChild.query(data) for tryChild in self.childs.values()]
				#print "Meet undefined feature"
				#print trys
				if len(trys) >= (2 * sum(trys)):
					return False
				else:
					return True
			else:
				return child.query(data)
		else:
			return self.flag

	def cut(self):
		if self.samples >= (2 * self.trues):
			self.flag = False
		else:
			self.flag = True

		self._childs = self.childs
		self.childs = {}

	def commit(self):
		del self._childs

	def revert(self):
		self.childs = self._childs
		del self._childs
		self.flag = None

def correctRate(node, data, label):
	right = sum([node.query(data[i]) == label[i] for i in range(len(label))])

	#print("Right: %s, Total: %s" % (right, len(label)))
	#print("Rate: %s" % (float(right) / len(label)))
	return float(right) / len(label)

allFeature = dict.fromkeys(range(len(trainSet[0])), True)
rootNode = Node(trainSet, trainLabel, allFeature)
bestRate = correctRate(rootNode, validationSet, validationLabel)

rates = []
rates.append((correctRate(rootNode, trainSet, trainLabel), bestRate, correctRate(rootNode, testSet, testLabel)))

print('Rates: TrainRate, ValidationRate, TestRate')
print("Init Best Rate: %s, %s, %s" % rates[-1])

def prune(node, root):
	for child in node.childs.values():
		if len(child.childs) > 0:
			prune(child, root)

	node.cut()

	rate = correctRate(root, validationSet, validationLabel)
	global bestRate

	if rate >= bestRate:
		node.commit()
		bestRate = rate
		rates.append((correctRate(root, trainSet, trainLabel), bestRate, correctRate(root, testSet, testLabel)))
		print("Best Rate: %s, %s, %s" % rates[-1])
	else:
		node.revert()

prune(rootNode, rootNode)
print("Final Best Rate: %s, %s, %s" % (correctRate(rootNode, trainSet, trainLabel), bestRate, correctRate(rootNode, testSet, testLabel)))

with open("result.json", 'w') as fout:
	fout.write(json.dumps(rates))
